# Tutorial — CODM English Patch v0.3 (edição final, descontinuada)

> **Aviso de risco:** este patch não oficial altera arquivos do CODM. A política pública da Activision prevê punições para software não autorizado que modifica dados do jogo e para engenharia reversa. Mesmo sendo uma tradução de textos, o patch não é garantidamente seguro: pode acionar verificações anti-cheat ou resultar em punição da conta, inclusive banimento. Use por sua conta e risco. Para reduzir ao máximo o risco da conta, jogue com uma instalação oficial sem modificações.

Este é o lançamento final. O projeto foi descontinuado e não terá novas atualizações, correções de compatibilidade ou suporte. O patch não foi autorizado pela Activision nem pela Tencent; a edição chinesa pode ter termos próprios. O usuário informou que a última cópia de validação funcionou, mas isso não garante compatibilidade com outras instalações ou atualizações.

## Antes de usar

- Leia o aviso de risco acima e a descrição do repositório.
- O pacote não instala o jogo completo; ele altera recursos de idioma de uma instalação existente.
- A versão é destinada ao build analisado e pode falhar após uma atualização.
- Feche o jogo e o emulador antes de qualquer alteração.
- Mantenha uma cópia dos arquivos originais e espaço livre para o backup.

## Aplicar o patch

1. Extraia o ZIP em uma pasta separada, sem sobrepor arquivos do jogo.
2. Execute `Apply-Translation.cmd`.
3. Informe a pasta que contém `CODM.exe` e `CODM_Data`, se o aplicador perguntar.
4. Anote o local do backup que o aplicador criar.

O patcher salva os arquivos anteriores em `Backups/<data-hora>/` antes de escrever. A aplicação do patch não elimina o risco de sanção.

## Restaurar os arquivos

1. Feche o jogo e o emulador.
2. Restaure os arquivos de `Backups/<data-hora>/` aos caminhos originais, mantendo a mesma estrutura de pastas; ou use a opção oficial de reparar/verificar arquivos do launcher.
3. Para jogar normalmente com o menor risco, confirme que a instalação oficial está sem modificações.

## Limites da tradução

O pacote cobre os recursos de idioma incluídos no build analisado. Texto enviado pelo servidor, embutido em imagens/vídeos ou guardado em recursos opacos pode continuar em chinês. A equivalência completa com o CODM Global não foi certificada, e futuras atualizações não serão acompanhadas.
