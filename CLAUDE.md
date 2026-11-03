# Wiki PepsRO: regras para o Claude

Wiki do **PepsRO**, servidor privado de Ragnarok Online (**Renovação**, rAthena), feita em **MkDocs Material** e publicada no GitHub Pages.

- Repositório: https://github.com/tioPeps/PepsRo-Wiki (branch `main`)
- Site: https://tiopeps.github.io/PepsRo-Wiki/
- Responder sempre em **português do Brasil**.

## Pastas

| Pasta | Regra |
|---|---|
| `D:\Servidor Ragnarok\Wiki PepsRO` | Área de trabalho. Pode criar e editar. |
| `D:\Servidor Ragnarok\PepsRo` | **SOMENTE LEITURA.** Nunca editar, criar, apagar, mover ou renomear nada lá, nem rodar comandos que alterem algo lá. Scripts só leem dele e gravam dentro da Wiki. |
| `C:\Users\Admin\Desktop\kawaROPatch` e `N:\` | Só leitura. |

## Fonte do conteúdo

- Os dados vêm **sempre da produção**: `D:\Servidor Ragnarok\PepsRo\rathena-producao` (o que os jogadores jogam). Nunca usar a homologação (`rathena\`): ela tem mudanças não publicadas e coisas só de teste (ex.: Zenny Mestre, cash de teste).
- Todo o conteúdo vem dos arquivos do PepsRO: item_db, mob_db, skill_db, drops, rates, configs e NPCs próprios (`npc/custom/pepsro`).
- **Não usar o KawaRO como referência para nada**: nem estrutura, nem estilo, nem textos, números ou sistemas.
- Informação que não está nos arquivos: **não inventar**. Marcar a página ou o trecho como "A preencher" (modelo abaixo) e perguntar ao usuário.
- **Nunca publicar** senhas, nada de `_segredos`, valores de senha do `conf/import`, IP do ZeroTier nem dados de contas de jogadores.

## O que pode ser editado

- Só o conteúdo de `docs/`, os `scripts/` e os `templates/`.
- **Não alterar** o tema, o `docs/stylesheets/pepsro.css` nem o `mkdocs.yml`, a não ser que o usuário peça. Exceção: ao criar uma página nova, ela precisa entrar no `nav` do `mkdocs.yml`; avisar o usuário.

## Estrutura de páginas

```
docs/
├─ index.md            Início
├─ comecar/            Início rápido, instalação e patcher, regras
├─ servidor/           Rates, mecânicas alteradas
├─ classes/            Visão geral, 1 página por classe (template), builds
├─ sistemas/           Sistemas próprios do PepsRO (Chefênia, Éden, Chapeleiro, lojas, encantador...)
├─ conteudo/           Instâncias, Além do Limite, Ilusão do Labirinto, Edda Biolab, MVPs
├─ eventos/            Devil Square, MvP Ladder, Bossnia, Cemitério Inquieto
├─ comandos.md, faq.md
└─ database/           GERADO por script: monstros, drops e mapas (itens ficam para depois)
```

- **Escritos à mão:** início rápido, rates, regras, classes, builds, sistemas, eventos, FAQ e comandos.
- **Gerados por script:** tudo em `docs/database/`, menos o `index.md`. Nunca editar páginas geradas à mão: muda-se o template ou o script e gera de novo.
- **Itens:** o usuário pediu para não colocar ainda.

## Templates fixos

| Template | Uso |
|---|---|
| `templates/monstro.md.j2` | Página de monstro (gerada) |
| `templates/item.md.j2` | Página de item (gerada, quando os itens entrarem) |
| `templates/classe.md` | Página de classe (copiar e preencher à mão, mesma ordem de seções) |

Modelo de trecho sem informação:

```markdown
!!! warning "A preencher"
    O que falta e de onde deveria vir.
```

## Padrão visual

- **Verde** dominante (títulos, cabeçalho, tabelas), **preto** como base, **vermelho** só em alertas (`warning`/`danger`), **azul** só em links. Cores definidas em `docs/stylesheets/pepsro.css` (variáveis `--pepsro-*`).
- Modo escuro por padrão (`slate`), com botão para o claro. Busca em português ligada.
- Boa leitura no celular: tabelas com rolagem horizontal, frases curtas, sem tabelas largas demais.
- Admonitions: `tip` para dicas, `warning` para "A preencher" e cuidados, `danger` para o que pode fazer o jogador perder algo.

## Gerador de dados (`scripts/gerar.py`)

1. Lê os YAML do rAthena seguindo os `Footer/Imports` (primeiro `db/re`, depois `db/import`) e junta campo a campo pelo `Id`, como o rAthena faz. Os spawns (`npc/re/mobs`, `npc/custom/pepsro`) e o `mob_skill_db` são TXT.
2. Nomes em português: `SystemEN\itemInfo_C.lua`, depois `itemInfo_PT.lua` (cliente), depois bRO (`_download\bro`), por último o nome em inglês do rAthena.
3. Chances de drop já com as rates reais da produção (`conf/import/battle_conf.txt`: 15x, cartas fixas em 2%, equipamento no mínimo 0,5%).
4. Grava só em `docs/database/` com os templates Jinja2.

## Rotina

```bash
.venv\Scripts\python scripts\gerar.py
.venv\Scripts\python -m mkdocs build --strict
.venv\Scripts\python -m mkdocs serve
```

- O build tem que passar com `--strict` antes de qualquer commit.
- As páginas geradas são commitadas (o GitHub Actions não tem acesso ao servidor).
- O deploy é automático: push na `main` → `.github/workflows/deploy.yml` → GitHub Pages.
- Commit e push só com o OK do usuário. Conta `tioPeps`, e-mail `tioPeps@users.noreply.github.com` (nunca o e-mail pessoal). O `git push` precisa do terminal interativo do usuário para o login do GitHub.
- Trabalhar em etapas curtas e avisar o usuário ao fim de cada uma.
