# CODM English Patch

Ferramenta comunitária para aplicar a tradução inglesa da interface do cliente chinês de Call of Duty: Mobile no Windows.

## Estado atual

- A versão 0.1 contém o catálogo que o usuário confirmou funcionando.
- O catálogo de referência tem o SHA-256 `626d73a33c935dafc139635cb995a8ea717b4054359789f0a0da909af072f127`.
- O aplicador contém 130.652 pares de tradução conhecidos para reaplicação em atualizações compatíveis.
- O checkout deste repositório contém o código e a documentação. O pacote completo precisa ser distribuído como um arquivo de Release; arquivos do jogo e o runtime não são armazenados no histórico Git.

## Instalação do pacote

O pacote completo precisa conter `Apply-Translation.cmd`, `Apply-Translation.py`, `translations.json.gz`, `Payload/` e `Runtime/`.

1. Feche o jogo e o emulador.
2. Extraia a pasta `CODM-English-Patch` dentro do diretório do jogo, ou mantenha-a em outro lugar.
3. Execute `Apply-Translation.cmd`.
4. Se a pasta do pacote estiver fora do jogo, informe o caminho da pasta CODM quando solicitado. O aplicador salva esse caminho em `GamePath.txt`.

## Atualizações do jogo

Depois de cada atualização, feche o jogo e execute `Apply-Translation.cmd` novamente. O aplicador reaplica as traduções conhecidas ao catálogo se o formato ainda for compatível e salva cópias de segurança em `Backups/` antes de gravar.

Se o catálogo mudar de formato ou nenhum texto conhecido for encontrado, o aplicador interrompe a operação sem alterar os arquivos do jogo. Textos introduzidos numa atualização precisam ser traduzidos e incluídos em uma nova versão do pacote. A reaplicação é manual; não há garantia de compatibilidade com toda atualização futura.

## Arquivos do pacote

- `Apply-Translation.py`: valida e atualiza o catálogo, preservando os outros arquivos internos.
- `Apply-Translation.cmd`: inicia o aplicador no Windows.
- `manifest.json`: hashes e limites da versão atual do pacote.
- `GamePath.example.txt`: exemplo vazio para configuração local.
- `Payload/`, `Runtime/`, `translations.json.gz`, `GamePath.txt` e `Backups/`: dados locais/de Release, ignorados pelo Git.

O pacote atua na interface. Ele não altera login, servidores, backend, proteções ou arquivos de partidas. Não contém um cliente do jogo completo.

## Integridade

O aplicador usa o runtime CPython 3.15 que acompanha o pacote completo; não requer uma instalação separada de Python. Os hashes dos arquivos distribuídos devem corresponder aos valores de `manifest.json`.

## Licença e conteúdo do jogo

Este repositório ainda não declara uma licença de uso. O pacote de Release pode conter arquivos derivados do cliente do jogo; esses arquivos não são adicionados aos commits do repositório.
