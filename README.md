![alt text](static/img/capaReadme.jpg)
### Curso Técnico de Desenvolvimento de Sistemas - Senai Itapeva
# EmpreGO

**Descrição:**  
O projeto EmpreGO é uma plataforma para auxiliar na busca e divulgação de oportunidades de emprego na cidade de Itapeva-SP. Ele visa facilitar a conexão entre empresas e candidatos, promovendo a visualização e gerenciamento de vagas disponíveis na região.

## Índice
- [Tecnologias](#tecnologias-utilizadas)
- [Status](#status)
- [Funcionalidades](#funcionalidades)
- [Detalhes Técnicos](#detalhes-técnicos)
- [Autores](#autores)
- [Licença](#licença)

## Status
🟡 Projeto em construção 🟡

## Funcionalidades
- **Usuários/Visitantes:**
  - Visualizar vagas disponíveis.
  - Pesquisar vagas por palavras-chave.
  - Enviar currículo para uma vaga específica.
  - Botão "Candidatar-se" só aparece para visitantes que não estão logados em nenhuma conta.

- **Empresas:**
  - Cadastrar-se e fazer login.
  - Cadastrar novas vagas de emprego.
  - Editar informações e excluir vagas cadastradas.
  - Visualizar currículos recebidos para as vagas.

- **Administrador:**
  - Adicionar, editar ou excluir empresas.
  - Gerenciar status das empresas (habilitar/desabilitar).
  - Gerenciar vagas (criar, editar, excluir, habilitar/desabilitar).

## Detalhes Técnicos

### Sessões de Login
O sistema agora gerencia sessões separadas para diferentes tipos de usuários:
- **Administração**: Utiliza a variável de sessão `admin_logged`.
- **Empresas**: Utiliza a variável de sessão `company_logged`.
- **Usuários Normais (Candidatos)**: Utiliza a variável de sessão `user_logged`.

### Verificação do Botão "Candidatar-se"
No template `sobre_vaga.html`, o botão "Candidatar-se" é exibido apenas para visitantes (usuários que não estão logados). Isso é controlado por verificações de sessão diretamente no código do template e reforçado por validações no backend.

## Tecnologias Utilizadas
**Linguagem/Frameworks:**

![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JAVASCRIPT](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)
![BOOTSTRAP](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)
![PYTHON](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![FLASK](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)

## Autores
- Douglas Bueno - [GitHub](https://github.com/DouglasBueno11) - douglas.bueno.senai@gmail.com

## Licença
Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para mais detalhes.