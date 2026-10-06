<#
  Compara todos os repositorios de C:\DEV com o GitHub.

  Uso:
    .\verificar-repos.ps1           -> so mostra o estado (fetch + status, nao altera nada)
    .\verificar-repos.ps1 -Pull     -> tambem faz pull nos que estao atras E sem alteracoes locais
    .\verificar-repos.ps1 -Clonar   -> tambem clona os repos do GitHub que ainda nao existem em C:\DEV

  Repos com alteracoes locais, commits nao enviados ou divergentes NUNCA sao alterados:
  o script so avisa, para resolver manualmente.
#>
param(
    [switch]$Pull,
    [switch]$Clonar,
    [string]$Raiz = 'C:\DEV',
    [string]$Conta = 'SkinDevX'
)

$env:GIT_TERMINAL_PROMPT = '0'
$resultado = @()

foreach ($d in Get-ChildItem $Raiz -Directory) {
    $p = $d.FullName
    if (-not (Test-Path "$p\.git")) { continue }

    $branch = git -C $p rev-parse --abbrev-ref HEAD 2>$null
    git -C $p fetch --quiet --prune 2>$null
    $fetchOk = ($LASTEXITCODE -eq 0)

    $alterados = (git -C $p status --porcelain 2>$null | Measure-Object).Count
    $atras = 0; $frente = 0; $temUpstream = $true
    $ab = git -C $p rev-list --left-right --count 'HEAD...@{u}' 2>$null
    if ($LASTEXITCODE -eq 0 -and $ab) {
        $partes = $ab -split '\s+'
        $frente = [int]$partes[0]; $atras = [int]$partes[1]
    } else { $temUpstream = $false }

    if (-not $fetchOk)          { $estado = 'ERRO NO FETCH' }
    elseif (-not $temUpstream)  { $estado = 'SEM BRANCH REMOTA' }
    elseif ($frente -gt 0 -and $atras -gt 0) { $estado = 'DIVERGENTE' }
    elseif ($alterados -gt 0)   { $estado = 'ALTERACOES LOCAIS' }
    elseif ($frente -gt 0)      { $estado = 'FALTA PUSH' }
    elseif ($atras -gt 0)       { $estado = 'ATRAS (precisa pull)' }
    else                        { $estado = 'OK' }

    if ($Pull -and $estado -eq 'ATRAS (precisa pull)') {
        git -C $p pull --ff-only --quiet 2>$null
        if ($LASTEXITCODE -eq 0) { $estado = "ATUALIZADO (+$atras commits)"; $atras = 0 }
        else { $estado = 'PULL FALHOU' }
    }

    $resultado += [pscustomobject]@{
        Repo = $d.Name; Branch = $branch; Atras = $atras; Frente = $frente
        Alterados = $alterados; Estado = $estado
    }
}

$resultado | Sort-Object Repo | Format-Table -AutoSize

# Repos que existem no GitHub mas nao estao clonados
if (Get-Command gh -ErrorAction SilentlyContinue) {
    $locais = $resultado.Repo
    $remotos = gh repo list $Conta --limit 200 --json name --jq '.[].name' 2>$null
    $faltando = $remotos | Where-Object { $locais -notcontains $_ } | Sort-Object
    if ($faltando) {
        Write-Host "No GitHub mas nao clonados em ${Raiz}:" -ForegroundColor Yellow
        foreach ($n in $faltando) {
            if ($Clonar) {
                git clone --quiet "https://github.com/$Conta/$n.git" (Join-Path $Raiz $n)
                if ($LASTEXITCODE -eq 0) { Write-Host "  $n  -> clonado" -ForegroundColor Green }
                else { Write-Host "  $n  -> FALHOU" -ForegroundColor Red }
            } else { Write-Host "  $n" }
        }
        if (-not $Clonar) { Write-Host "(rode com -Clonar para baixar)" }
    } else { Write-Host "Todos os repos do GitHub ($Conta) estao clonados." -ForegroundColor Green }
}

$problemas = $resultado | Where-Object { $_.Estado -notmatch '^(OK|ATUALIZADO)' }
if ($problemas) { Write-Host "`nAtencao: $($problemas.Count) repo(s) precisam de acao (veja a coluna Estado)." -ForegroundColor Yellow }
else { Write-Host "`nTudo sincronizado com o GitHub." -ForegroundColor Green }
