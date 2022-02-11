CREATE TABLE IF NOT EXISTS sesion(
    id serial primary key,
    sesion_number int
);
CREATE TABLE IF NOT EXISTS votacion(
    id serial primary key,
    sesion_id int not null,
    votacion_number int not null,
    fecha date not null,
    titulo text not null,
    textoExpediente text not null,
    tituloSubGrupo text not null,
    textoSubGrupo text not null,
    constraint fk_sesion FOREIGN KEY(sesion_id) references sesion(id)
);
CREATE TABLE IF NOT EXISTS votos_resumido(
    id serial primary key,
    votacion_id int not null,
    grupo text not null,
    a_favor int not null,
    en_contra int not null,
    abstencion int not null,
    nsnc int not null,
    constraint fk_votacion FOREIGN KEY (votacion_id) references votacion(id)
);

CREATE TABLE IF NOT EXISTS votos_detallado(
    id serial primary key,
    votacion_id int not null,
    asiento int,
    diputado text not null,
    grupo text not null,
    voto text not null,
    constraint fk_votacion FOREIGN KEY (votacion_id) references votacion(id)
);

