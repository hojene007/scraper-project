use einformaDB;

create table generalInfo(
actividadInforma varchar(9999),
CIFNIF varchar(9999),
CNAE2009 varchar(9999),
Denom varchar(9999),
DomicAnter varchar(9999),
DomicSocial varchar(9999),
Fax varchar(9999),
Marcas varchar(9999),
DUNS varchar(9999),
ObjectoSocial varchar(9999),
SIC varchar(9999),
Situation varchar(9999),
Telefono varchar(9999),
URL varchar(9999),
otraInfo varchar(9999999)
);

create table generalInfo(
ActividadInforma nvarchar(200) ,
CIFNIF nvarchar(99),
CNAE2009 nvarchar(50),
Denominacin nvarchar(99),
DomicilioAnterior nvarchar(200),
DomicilioSocial nvarchar(200),
Fax nvarchar(200),
MarcasRegistradas nvarchar(999),
NmeroDUNS nvarchar(99),
ObjetoSocial nvarchar(400),
SIC nvarchar(999),
SituacindelaEmpresa nvarchar(200),
Telfono nvarchar(99),
URL nvarchar(999),
otraInfo nvarchar(9999),

primary key (Denominacin));

select*from einformaDB.eInforma_Empresas limit 5;