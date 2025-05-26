--
-- PostgreSQL database dump
--

-- Dumped from database version 16.8
-- Dumped by pg_dump version 16.8

-- Started on 2025-05-13 23:02:39 MSK

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

--
-- TOC entry 3641 (class 1262 OID 16505)
-- Name: delivery; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE delivery WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'C';


ALTER DATABASE delivery OWNER TO postgres;

\connect delivery

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
-- TOC entry 217 (class 1259 OID 16521)
-- Name: address; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.address (
    id integer NOT NULL,
    city character varying(20),
    street character varying(30),
    house smallint,
    room smallint,
    user_id integer NOT NULL
);


ALTER TABLE public.address OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 16511)
-- Name: contacts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.contacts (
    id integer NOT NULL,
    telephone character varying(10),
    mail character varying(30),
    user_id integer NOT NULL
);


ALTER TABLE public.contacts OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16548)
-- Name: description; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.description (
    id smallint NOT NULL,
    containt text,
    k numeric,
    b numeric,
    j numeric,
    u numeric,
    weight smallint
);


ALTER TABLE public.description OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16578)
-- Name: order_details; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.order_details (
    order_id integer NOT NULL,
    product_id smallint NOT NULL,
    unit_price smallint NOT NULL,
    quantity smallint NOT NULL,
    discount real NOT NULL
);


ALTER TABLE public.order_details OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 16531)
-- Name: orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders (
    id integer NOT NULL,
    amount integer,
    user_id integer NOT NULL
);


ALTER TABLE public.orders OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16555)
-- Name: products; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.products (
    id smallint NOT NULL,
    name character varying(30) NOT NULL,
    stop_list boolean NOT NULL,
    price2 smallint NOT NULL,
    desc_id smallint NOT NULL
);


ALTER TABLE public.products OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 16506)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    name character varying(30)
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 3631 (class 0 OID 16521)
-- Dependencies: 217
-- Data for Name: address; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3630 (class 0 OID 16511)
-- Dependencies: 216
-- Data for Name: contacts; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3633 (class 0 OID 16548)
-- Dependencies: 219
-- Data for Name: description; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.description (id, containt, k, b, j, u, weight) VALUES (1, 'Ваш любимый Гранд Де Люкс теперь с острым перцем Халапеньо! Сочный бифштекс из натуральной говядины, приготовленный на гриле, карамелизованная булочка с кунжутом, два ломтика сыра Чеддер, свежий салат, кусочек помидора и лук, маринованные огурчики, кетчуп, горчица специальный соус и острый перец Халапеньо.', 571, 31, 31, 40, 256) ON CONFLICT DO NOTHING;
INSERT INTO public.description (id, containt, k, b, j, u, weight) VALUES (2, 'Нежная и изысканная приправа Шейк-Шейк со вкусом «Сметана-зелень». Добавь ее в Картофель Гранд Фри по вкусу. Просто засыпь Картофель и приправу в специальный пакет, потряси и шейкарно перекуси!', 376, 14, 23, 45, 187) ON CONFLICT DO NOTHING;
INSERT INTO public.description (id, containt, k, b, j, u, weight) VALUES (3, 'Эксклюзивный бургер от популярного актера Сергея Бурунова! Три сочных бифштекса из натуральной цельной говядины с тремя видами сыра: Чеддер, Эмменталь и пикантный сыр твердых сортов. А еще лук и два кусочка хрустящего маринованного огурчика на классической карамелизованной булочке, заправленные кетчупом и горчицей.', 571, 36, 32, 32, 224) ON CONFLICT DO NOTHING;


--
-- TOC entry 3635 (class 0 OID 16578)
-- Dependencies: 221
-- Data for Name: order_details; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3632 (class 0 OID 16531)
-- Dependencies: 218
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3634 (class 0 OID 16555)
-- Dependencies: 220
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.products (id, name, stop_list, price2, desc_id) VALUES (1, 'Гранд Де Люкс Халапеньо', false, 262, 1) ON CONFLICT DO NOTHING;
INSERT INTO public.products (id, name, stop_list, price2, desc_id) VALUES (2, 'Гранд Фри средний', false, 157, 2) ON CONFLICT DO NOTHING;
INSERT INTO public.products (id, name, stop_list, price2, desc_id) VALUES (3, 'Тройной Чизбургер Три Сыра', false, 432, 3) ON CONFLICT DO NOTHING;


--
-- TOC entry 3629 (class 0 OID 16506)
-- Dependencies: 215
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.users (id, name) VALUES (2143848793, 'Денис Макарцев') ON CONFLICT DO NOTHING;
INSERT INTO public.users (id, name) VALUES (864624636, 'OG_BoB') ON CONFLICT DO NOTHING;


--
-- TOC entry 3471 (class 2606 OID 16525)
-- Name: address address_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.address
    ADD CONSTRAINT address_pkey PRIMARY KEY (id);


--
-- TOC entry 3469 (class 2606 OID 16515)
-- Name: contacts contacts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contacts
    ADD CONSTRAINT contacts_pkey PRIMARY KEY (id);


--
-- TOC entry 3475 (class 2606 OID 16554)
-- Name: description description_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.description
    ADD CONSTRAINT description_pkey PRIMARY KEY (id);


--
-- TOC entry 3479 (class 2606 OID 16582)
-- Name: order_details order_details_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_details
    ADD CONSTRAINT order_details_pkey PRIMARY KEY (order_id, product_id);


--
-- TOC entry 3473 (class 2606 OID 16535)
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


--
-- TOC entry 3477 (class 2606 OID 16559)
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- TOC entry 3467 (class 2606 OID 16510)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 3480 (class 2606 OID 16516)
-- Name: contacts order_details_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contacts
    ADD CONSTRAINT order_details_order_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 3481 (class 2606 OID 16526)
-- Name: address order_details_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.address
    ADD CONSTRAINT order_details_order_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 3482 (class 2606 OID 16536)
-- Name: orders order_details_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT order_details_order_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 3483 (class 2606 OID 16560)
-- Name: products order_details_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT order_details_order_id_fkey FOREIGN KEY (desc_id) REFERENCES public.description(id);


--
-- TOC entry 3484 (class 2606 OID 16583)
-- Name: order_details order_details_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_details
    ADD CONSTRAINT order_details_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id);


--
-- TOC entry 3485 (class 2606 OID 16588)
-- Name: order_details order_details_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_details
    ADD CONSTRAINT order_details_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


-- Completed on 2025-05-13 23:02:39 MSK

--
-- PostgreSQL database dump complete
--

-- Новая таблица для платежей 

CREATE TABLE public.payments (
    id SERIAL PRIMARY KEY,
    user_id integer NOT NULL REFERENCES public.users(id),
    order_id integer NOT NULL REFERENCES public.orders(id),
    amount integer NOT NULL,
    status varchar(20) NOT NULL DEFAULT 'pending',
    payment_date timestamp DEFAULT CURRENT_TIMESTAMP,
    transaction_id varchar(50)
);
