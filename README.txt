SQL utilizado na criação do banco de dados que foi usado neste programa.
Foi utilizando o MySQL.

CREATE DATABASE mylist;

create table lista(
	ID int auto_increment primary key,
    T_COMPRA varchar(233),
    N_VALOR int,
    T_DETALHE varchar(233)
    
);
