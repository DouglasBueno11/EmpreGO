create database emprego;
use emprego;

create table empresa(
    id_empresa int primary key auto_increment,
    nome_empresa varchar(100) not null,
    cnpj char(14) not null,
    telefone char(11) not null,
    email varchar(100) unique not null, 
    senha varchar(30) not null, 
    status enum('ativa','inativa') default 'ativa' not null 
);

create table vaga(
    id_vaga int primary key auto_increment,
    titulo varchar(100) not null,
    descrição text not null,
    formato enum('Presencial','Híbrido','Remoto') not null,
    tipo enum('CLT','PJ') not null,
    local varchar(100),
    salario varchar(10),
    id_empresa int not null,
    status enum('ativa','inativa') default 'ativa' not null,
    foreign key (id_empresa) references empresa (id_empresa)
);

-- Inserção de 3 empresas
INSERT INTO empresa (nome_empresa, cnpj, telefone, email, senha, status)
VALUES
('Tech Solutions', '12345678000199', '11987654321', 'contato@techsolutions.com.br', 'senha123', 'ativa'),
('Innova Consulting', '98765432000177', '21987654321', 'info@innovaconsulting.com', 'senha456', 'ativa'),
('Future Devs', '45678912000188', '31987654321', 'hr@futuredevs.com', 'senha789', 'ativa');

-- Inserção de 5 vagas para a empresa "Tech Solutions" (id_empresa = 1)
INSERT INTO vaga (titulo, descricao, formato, tipo, local, salario, id_empresa, status)
VALUES
('Desenvolvedor Frontend', 'Desenvolvimento de interfaces web com foco em usabilidade e performance.', 'Remoto', 'CLT', 'Remoto', 'R$ 5000', 1, 'ativa'),
('Desenvolvedor Backend', 'Implementação de APIs e manutenção de servidores.', 'Híbrido', 'CLT', 'São Paulo - SP', 'R$ 6000', 1, 'ativa'),
('Analista de Dados', 'Análise de grandes volumes de dados e geração de relatórios.', 'Presencial', 'CLT', 'São Paulo - SP', 'R$ 5500', 1, 'ativa'),
('Gerente de Projetos', 'Gestão de equipes e acompanhamento de cronogramas.', 'Híbrido', 'PJ', 'São Paulo - SP', 'R$ 8000', 1, 'ativa'),
('Designer UX/UI', 'Criação de interfaces intuitivas e focadas na experiência do usuário.', 'Remoto', 'PJ', 'Remoto', 'R$ 4500', 1, 'ativa');

-- Inserção de 5 vagas para a empresa "Innova Consulting" (id_empresa = 2)
INSERT INTO vaga (titulo, descricao, formato, tipo, local, salario, id_empresa, status)
VALUES
('Consultor de TI', 'Consultoria em infraestrutura e suporte técnico.', 'Presencial', 'CLT', 'Rio de Janeiro - RJ', 'R$ 7000', 2, 'ativa'),
('Especialista em Segurança da Informação', 'Responsável por garantir a segurança dos dados e infraestrutura.', 'Híbrido', 'CLT', 'Rio de Janeiro - RJ', 'R$ 9000', 2, 'ativa'),
('DevOps Engineer', 'Automatização de processos e gestão de infraestrutura em nuvem.', 'Remoto', 'PJ', 'Remoto', 'R$ 8500', 2, 'ativa'),
('Scrum Master', 'Facilitação de equipes ágeis utilizando Scrum.', 'Remoto', 'PJ', 'Remoto', 'R$ 7000', 2, 'ativa'),
('Analista de Sistemas', 'Análise e desenvolvimento de sistemas corporativos.', 'Presencial', 'CLT', 'Rio de Janeiro - RJ', 'R$ 6000', 2, 'ativa');

-- Inserção de 5 vagas para a empresa "Future Devs" (id_empresa = 3)
INSERT INTO vaga (titulo, descricao, formato, tipo, local, salario, id_empresa, status)
VALUES
('Programador Fullstack', 'Desenvolvimento de soluções completas, frontend e backend.', 'Híbrido', 'CLT', 'Belo Horizonte - MG', 'R$ 7000', 3, 'ativa'),
('Engenheiro de Software', 'Desenvolvimento de software e gestão de ciclo de vida de aplicações.', 'Presencial', 'CLT', 'Belo Horizonte - MG', 'R$ 9000', 3, 'ativa'),
('QA Tester', 'Testes automatizados e garantia de qualidade do software.', 'Remoto', 'CLT', 'Remoto', 'R$ 6000', 3, 'ativa'),
('Arquiteto de Soluções', 'Definição de arquitetura de sistemas e infraestrutura.', 'Híbrido', 'PJ', 'Belo Horizonte - MG', 'R$ 10000', 3, 'ativa'),
('Analista de Suporte', 'Atendimento a clientes e suporte técnico de sistemas.', 'Presencial', 'CLT', 'Belo Horizonte - MG', 'R$ 4000', 3, 'ativa');
