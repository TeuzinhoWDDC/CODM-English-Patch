# Tutorial de instalação — CODM English Patch v0.2

Este tutorial aplica a tradução à instalação existente do cliente chinês de
Call of Duty: Mobile para Windows. O patch não instala o jogo.

## Antes de começar

- Use o jogo que já está instalado no seu computador.
- Feche CODM e o emulador completamente.
- Extraia o ZIP do patch para uma pasta separada. Não extraia por cima dos
  arquivos do jogo.
- Deixe espaço livre para o backup. O aplicador salva os arquivos originais
  antes de substituí-los.

## Aplicar a tradução

1. Abra a pasta extraída e execute `Apply-Translation.cmd`.
2. Se aparecer a pergunta sobre o caminho, cole a pasta que contém `CODM.exe`
   e `CODM_Data`. Exemplo:

   `F:\CODMGameApps\CN\emulator\Extract\CODM`

3. Pressione Enter e aguarde a mensagem `Tradução aplicada`.
4. Anote o caminho da cópia de segurança exibido no final.
5. Inicie o jogo do modo habitual e confira o lobby e os menus.

O caminho escolhido fica salvo em `GamePath.txt`. Para selecionar outra cópia
do jogo na próxima execução, apague o conteúdo desse arquivo antes de abrir o
aplicador.

## Restaurar os arquivos originais

1. Feche CODM e o emulador.
2. Na pasta do patch, abra `Backups` e depois a pasta de data e hora indicada
   pelo aplicador.
3. Copie cada arquivo do backup de volta ao mesmo caminho dentro da pasta do
   jogo, substituindo a versão traduzida. O backup mantém a mesma estrutura de
   pastas; por exemplo, restaure `CODM_Data\StreamingAssets\0db.bytes` no
   mesmo local da instalação.

Mantenha a pasta do patch e os backups até terminar seus testes.

## Depois de uma atualização do jogo

Feche o jogo e execute o aplicador novamente. Ele tenta reconhecer o catálogo
e reaplicar as frases conhecidas. Se o jogo tiver mudado o formato, a execução
deve informar que não foi possível aplicar; não force a cópia do arquivo de
outra versão. Uma atualização pode exigir uma nova versão do patch.

## Problemas comuns

- **O caminho não foi encontrado:** informe a pasta que contém `CODM_Data`,
  não a própria pasta `CODM_Data`.
- **Nenhum texto conhecido foi encontrado:** o catálogo provavelmente é de
  outra versão ou teve o formato alterado. O aplicador não grava um catálogo
  quando não encontra frases compatíveis.
- **Ainda vejo chinês:** esta versão cobre o catálogo principal de idioma.
  Texto vindo do servidor, de tabelas ainda não decodificadas ou incorporado
  em imagens e vídeos pode permanecer no idioma original.
- **Quero relatar um erro:** envie a tela e o `Last-Run-Report.txt`, se houver.
  Nunca envie senha, token ou dados da conta.

## Cobertura e limites

No catálogo principal do build analisado, v0.2 substitui 164.256 registros
com caracteres chineses, correspondentes a 130.989 frases únicas. O catálogo
resultante não contém caracteres chineses. As traduções herdadas da v0.1 não
foram todas revisadas manualmente, e a equivalência exata com o COD Mobile
Global não foi certificada.
