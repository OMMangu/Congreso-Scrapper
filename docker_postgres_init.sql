CREATE TABLE IF NOT EXISTS sesion(
    id serial primary key,
    sesion_number int8 UNIQUE
);
CREATE TABLE IF NOT EXISTS votacion (
	id bigserial NOT NULL,
	sesion_id int8 NOT NULL,
	votacion_number int4 NOT NULL,
	fecha date NOT NULL,
	titulo text NOT NULL,
	textoexpediente text NOT NULL,
	titulosubgrupo text NOT NULL,
	textosubgrupo text NOT NULL,
	CONSTRAINT votacion_pkey PRIMARY KEY (id)
	);
ALTER TABLE votacion ADD CONSTRAINT fk_sesion FOREIGN KEY(sesion_id) references sesion(sesion_number);

CREATE TABLE IF NOT EXISTS votos_resumido(
	id bigserial NOT NULL,
	votacion_id int8 NOT NULL,
	grupo text NOT NULL,
	a_favor text NOT NULL,
	en_contra text NOT NULL,
	abstencion text NOT NULL,
	nsnc text NOT NULL,
	CONSTRAINT votos_resumido_pkey PRIMARY KEY (id)
);
ALTER TABLE public.votos_resumido ADD CONSTRAINT fk_votacion_resumida FOREIGN KEY (votacion_id) REFERENCES public.votacion(id);

CREATE TABLE IF NOT EXISTS votos_detallado(
	id bigserial NOT NULL,
	votacion_id int8 NOT NULL,
	asiento int4 NULL,
	diputado text NOT NULL,
	grupo text NOT NULL,
	voto text NOT NULL,
	CONSTRAINT votos_detallado_pkey PRIMARY KEY (id)
);
ALTER TABLE votos_detallado ADD CONSTRAINT fk_votacion FOREIGN KEY (votacion_id) REFERENCES public.votacion(id);

