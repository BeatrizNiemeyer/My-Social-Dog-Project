--
-- PostgreSQL database dump
--

-- Dumped from database version 13.5 (Ubuntu 13.5-2.pgdg20.04+1)
-- Dumped by pg_dump version 13.5 (Ubuntu 13.5-2.pgdg20.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: dogs; Type: TABLE; Schema: public; Owner: hackbright
--

CREATE TABLE public.dogs (
    dog_id integer NOT NULL,
    user_id integer,
    dog_name character varying NOT NULL,
    dog_age integer NOT NULL,
    dog_size character varying NOT NULL,
    dog_breed character varying,
    dog_photo character varying
);


ALTER TABLE public.dogs OWNER TO hackbright;

--
-- Name: dogs_dog_id_seq; Type: SEQUENCE; Schema: public; Owner: hackbright
--

CREATE SEQUENCE public.dogs_dog_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dogs_dog_id_seq OWNER TO hackbright;

--
-- Name: dogs_dog_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hackbright
--

ALTER SEQUENCE public.dogs_dog_id_seq OWNED BY public.dogs.dog_id;


--
-- Name: messages; Type: TABLE; Schema: public; Owner: hackbright
--

CREATE TABLE public.messages (
    message_id integer NOT NULL,
    sender_id integer,
    receiver_id integer,
    message_body character varying NOT NULL,
    message_date timestamp without time zone
);


ALTER TABLE public.messages OWNER TO hackbright;

--
-- Name: messages_message_id_seq; Type: SEQUENCE; Schema: public; Owner: hackbright
--

CREATE SEQUENCE public.messages_message_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.messages_message_id_seq OWNER TO hackbright;

--
-- Name: messages_message_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hackbright
--

ALTER SEQUENCE public.messages_message_id_seq OWNED BY public.messages.message_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: hackbright
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    fullname character varying NOT NULL,
    email character varying NOT NULL,
    password character varying NOT NULL,
    address character varying NOT NULL,
    longitude double precision,
    latitude double precision
);


ALTER TABLE public.users OWNER TO hackbright;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: hackbright
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_user_id_seq OWNER TO hackbright;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hackbright
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: dogs dog_id; Type: DEFAULT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.dogs ALTER COLUMN dog_id SET DEFAULT nextval('public.dogs_dog_id_seq'::regclass);


--
-- Name: messages message_id; Type: DEFAULT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.messages ALTER COLUMN message_id SET DEFAULT nextval('public.messages_message_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: dogs; Type: TABLE DATA; Schema: public; Owner: hackbright
--

COPY public.dogs (dog_id, user_id, dog_name, dog_age, dog_size, dog_breed, dog_photo) FROM stdin;
1	1	Cooper	2	medium	goldendoodle	\N
2	2	Copper	2	large	goldendoodle	\N
3	3	Penny	0	small	mix	\N
4	4	Boone	5	large	pitbull	\N
5	5	Rudy	8	small	corgi	\N
6	6	Lily	0	small	mix	\N
\.


--
-- Data for Name: messages; Type: TABLE DATA; Schema: public; Owner: hackbright
--

COPY public.messages (message_id, sender_id, receiver_id, message_body, message_date) FROM stdin;
1	1	2	Hi Ray!!	2022-03-21 21:15:22.54403
2	1	1	Hi!!	2022-03-21 21:24:35.609385
3	1	1	Hi!!	2022-03-21 21:31:27.576487
4	1	1	hello	2022-03-21 21:33:56.105727
5	1	2	Hi!	2022-03-21 21:35:12.139235
6	1	3	Hello Beth!	2022-03-21 21:35:29.779378
7	1	3	How are you?\r\n	2022-03-21 21:35:38.32343
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: hackbright
--

COPY public.users (user_id, fullname, email, password, address, longitude, latitude) FROM stdin;
1	Bia	bia@hb.com	123	7 N 8th st Richmond VA 23219	-77.43660550341482	37.5392443010174
2	Ray	ray@hb.com	123	9001 Staples Mill Rd, Henrico, VA 23228	-77.51126620527393	37.639684450000004
3	Beth	beth@hb.com	123	5401 W Broad St, Richmond, VA 23230	-77.495084	37.5830383
4	Mark	mark@hb.com	123	2801 E Franklin St, Richmond, VA 23223	-77.41769	37.528107
5	Steve	steve@hb.com	123	11698 W Broad St, Richmond, VA 23233	-77.495084	37.5830383
6	Lize	lize@hb.com	123	12200 Wegmans Blvd, Henrico, VA 23233	-77.6353943	37.6630212
\.


--
-- Name: dogs_dog_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hackbright
--

SELECT pg_catalog.setval('public.dogs_dog_id_seq', 6, true);


--
-- Name: messages_message_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hackbright
--

SELECT pg_catalog.setval('public.messages_message_id_seq', 7, true);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hackbright
--

SELECT pg_catalog.setval('public.users_user_id_seq', 6, true);


--
-- Name: dogs dogs_pkey; Type: CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.dogs
    ADD CONSTRAINT dogs_pkey PRIMARY KEY (dog_id);


--
-- Name: messages messages_pkey; Type: CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (message_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: dogs dogs_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.dogs
    ADD CONSTRAINT dogs_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: messages messages_receiver_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_receiver_id_fkey FOREIGN KEY (receiver_id) REFERENCES public.users(user_id);


--
-- Name: messages messages_sender_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_sender_id_fkey FOREIGN KEY (sender_id) REFERENCES public.users(user_id);


--
-- PostgreSQL database dump complete
--

