--
-- PostgreSQL database dump
--

-- Dumped from database version 13.20 (Raspbian 13.20-0+deb11u1)
-- Dumped by pg_dump version 17.4

-- Started on 2025-05-24 16:07:31

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
-- TOC entry 4 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -;
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO pi;

--
-- TOC entry 215 (class 1255 OID 24729)
-- Name: generate_offer_id(); Type: FUNCTION; Schema: public; Owner: pi
--

CREATE FUNCTION public.generate_offer_id() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  NEW."OfferID" := 'of-' || LPAD(NEXTVAL('offer_seq')::TEXT, 6, '0');
  RETURN NEW;
END;
$$;


ALTER FUNCTION public.generate_offer_id() OWNER TO pi;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 203 (class 1259 OID 16417)
-- Name: Clients; Type: TABLE; Schema: public; Owner: pi
--

CREATE TABLE public."Clients" (
    "ClientID" integer NOT NULL,
    "CompanyName" character varying(30) DEFAULT NULL::character varying,
    "CIF" character varying(9),
    "Address" character varying(20) DEFAULT NULL::character varying,
    "Email" character varying(20),
    "Phone" integer,
    "Contact" character varying(30) DEFAULT NULL::character varying
);


ALTER TABLE public."Clients" OWNER TO pi;

--
-- TOC entry 202 (class 1259 OID 16415)
-- Name: Clientes_ClienteID_seq; Type: SEQUENCE; Schema: public; Owner: pi
--

CREATE SEQUENCE public."Clientes_ClienteID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Clientes_ClienteID_seq" OWNER TO pi;

--
-- TOC entry 3093 (class 0 OID 0)
-- Dependencies: 202
-- Name: Clientes_ClienteID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pi
--

ALTER SEQUENCE public."Clientes_ClienteID_seq" OWNED BY public."Clients"."ClientID";


--
-- TOC entry 210 (class 1259 OID 24804)
-- Name: Clients_ClientID_seq; Type: SEQUENCE; Schema: public; Owner: pi
--

ALTER TABLE public."Clients" ALTER COLUMN "ClientID" ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."Clients_ClientID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 201 (class 1259 OID 16410)
-- Name: DeliveryNotes; Type: TABLE; Schema: public; Owner: pi
--

CREATE TABLE public."DeliveryNotes" (
    "DeliveryNoteID" character varying NOT NULL,
    "EmployeID" character varying,
    "ClientID" integer,
    "Date" date,
    "TotalPrice" integer
);


ALTER TABLE public."DeliveryNotes" OWNER TO pi;

--
-- TOC entry 208 (class 1259 OID 24671)
-- Name: Employes; Type: TABLE; Schema: public; Owner: pi
--

CREATE TABLE public."Employes" (
    "EmployeID" character varying(100) NOT NULL,
    "Name" character varying(25),
    "Family_name" character varying(50),
    "Email" character varying(80) DEFAULT NULL::character varying,
    "Rol" integer
);


ALTER TABLE public."Employes" OWNER TO pi;

--
-- TOC entry 204 (class 1259 OID 16423)
-- Name: Invoices; Type: TABLE; Schema: public; Owner: pi
--

CREATE TABLE public."Invoices" (
    "InvoiceID" character varying NOT NULL,
    "EmployeID" character varying,
    "ClientID" integer,
    "Date" date,
    "TotalPrice" integer
);


ALTER TABLE public."Invoices" OWNER TO pi;

--
-- TOC entry 205 (class 1259 OID 16428)
-- Name: Offers; Type: TABLE; Schema: public; Owner: pi
--

CREATE TABLE public."Offers" (
    "OfferID" character varying NOT NULL,
    "EmployeID" character varying,
    "ClientID" integer,
    "Date" date,
    "TotalPrice" integer
);


ALTER TABLE public."Offers" OWNER TO pi;

--
-- TOC entry 200 (class 1259 OID 16405)
-- Name: Orders; Type: TABLE; Schema: public; Owner: pi
--

CREATE TABLE public."Orders" (
    "OrderID" character varying NOT NULL,
    "EmployeID" character varying,
    "ClientID" integer,
    "Date" date,
    "TotalPrice" integer
);


ALTER TABLE public."Orders" OWNER TO pi;

--
-- TOC entry 213 (class 1259 OID 24816)
-- Name: ProdDn; Type: TABLE; Schema: public; Owner: pi
--

CREATE TABLE public."ProdDn" (
    "ProductID" integer NOT NULL,
    "DeliveryNoteID" character varying NOT NULL,
    "Quantity" integer NOT NULL
);


ALTER TABLE public."ProdDn" OWNER TO pi;

--
-- TOC entry 214 (class 1259 OID 24949)
-- Name: ProdInv; Type: TABLE; Schema: public; Owner: pi
--

CREATE TABLE public."ProdInv" (
    "ProductID" integer NOT NULL,
    "InvoiceID" character varying NOT NULL,
    "Quantity" integer
);


ALTER TABLE public."ProdInv" OWNER TO pi;

--
-- TOC entry 211 (class 1259 OID 24806)
-- Name: ProdOfe; Type: TABLE; Schema: public; Owner: pi
--

CREATE TABLE public."ProdOfe" (
    "ProductID" integer NOT NULL,
    "Quantity" integer,
    "OfferID" character varying NOT NULL
);


ALTER TABLE public."ProdOfe" OWNER TO pi;

--
-- TOC entry 212 (class 1259 OID 24811)
-- Name: ProdOrd; Type: TABLE; Schema: public; Owner: pi
--

CREATE TABLE public."ProdOrd" (
    "ProductID" integer NOT NULL,
    "Quantity" integer NOT NULL,
    "OrderID" character varying NOT NULL
);


ALTER TABLE public."ProdOrd" OWNER TO pi;

--
-- TOC entry 207 (class 1259 OID 16445)
-- Name: Products; Type: TABLE; Schema: public; Owner: pi
--

CREATE TABLE public."Products" (
    "ProductID" integer NOT NULL,
    "Name" character varying(30),
    "Description" character varying(50),
    "Stock" integer,
    "MaxStock" integer,
    "MinStock" integer,
    "Location" character varying(30),
    "PurchasePrice" numeric,
    "SellPrice" numeric
);


ALTER TABLE public."Products" OWNER TO pi;

--
-- TOC entry 206 (class 1259 OID 16443)
-- Name: Productos_ProductoID_seq; Type: SEQUENCE; Schema: public; Owner: pi
--

CREATE SEQUENCE public."Productos_ProductoID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Productos_ProductoID_seq" OWNER TO pi;

--
-- TOC entry 3094 (class 0 OID 0)
-- Dependencies: 206
-- Name: Productos_ProductoID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pi
--

ALTER SEQUENCE public."Productos_ProductoID_seq" OWNED BY public."Products"."ProductID";


--
-- TOC entry 209 (class 1259 OID 24715)
-- Name: offer_seq; Type: SEQUENCE; Schema: public; Owner: pi
--

CREATE SEQUENCE public.offer_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.offer_seq OWNER TO pi;

--
-- TOC entry 2912 (class 2604 OID 16448)
-- Name: Products ProductID; Type: DEFAULT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public."Products" ALTER COLUMN "ProductID" SET DEFAULT nextval('public."Productos_ProductoID_seq"'::regclass);


--
-- TOC entry 2919 (class 2606 OID 24864)
-- Name: DeliveryNotes Albaran_pkey; Type: CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public."DeliveryNotes"
    ADD CONSTRAINT "Albaran_pkey" PRIMARY KEY ("DeliveryNoteID");


--
-- TOC entry 2921 (class 2606 OID 24793)
-- Name: Clients Clientes_pkey; Type: CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public."Clients"
    ADD CONSTRAINT "Clientes_pkey" PRIMARY KEY ("ClientID");


--
-- TOC entry 2929 (class 2606 OID 24709)
-- Name: Employes Employes_pkey; Type: CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public."Employes"
    ADD CONSTRAINT "Employes_pkey" PRIMARY KEY ("EmployeID");


--
-- TOC entry 2923 (class 2606 OID 24921)
-- Name: Invoices Factura_pkey; Type: CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public."Invoices"
    ADD CONSTRAINT "Factura_pkey" PRIMARY KEY ("InvoiceID");


--
-- TOC entry 2925 (class 2606 OID 24718)
-- Name: Offers Oferta_pkey; Type: CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public."Offers"
    ADD CONSTRAINT "Oferta_pkey" PRIMARY KEY ("OfferID");


--
-- TOC entry 2915 (class 2606 OID 24750)
-- Name: Orders Pedido_pkey; Type: CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public."Orders"
    ADD CONSTRAINT "Pedido_pkey" PRIMARY KEY ("OrderID");


--
-- TOC entry 2937 (class 2606 OID 24903)
-- Name: ProdDn ProdDn_pkey; Type: CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public."ProdDn"
    ADD CONSTRAINT "ProdDn_pkey" PRIMARY KEY ("ProductID", "DeliveryNoteID");


--
-- TOC entry 2939 (class 2606 OID 24956)
-- Name: ProdInv ProdInv_pkey; Type: CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public."ProdInv"
    ADD CONSTRAINT "ProdInv_pkey" PRIMARY KEY ("ProductID", "InvoiceID");


--
-- TOC entry 2931 (class 2606 OID 24852)
-- Name: ProdOfe ProdOfe_pkey; Type: CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public."ProdOfe"
    ADD CONSTRAINT "ProdOfe_pkey" PRIMARY KEY ("ProductID", "OfferID");


--
-- TOC entry 2935 (class 2606 OID 24850)
-- Name: ProdOrd ProdOrd_pkey; Type: CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public."ProdOrd"
    ADD CONSTRAINT "ProdOrd_pkey" PRIMARY KEY ("ProductID", "OrderID");


--
-- TOC entry 2927 (class 2606 OID 16450)
-- Name: Products Productos_pkey; Type: CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public."Products"
    ADD CONSTRAINT "Productos_pkey" PRIMARY KEY ("ProductID");


--
-- TOC entry 2916 (class 1259 OID 24789)
-- Name: fki_ClientID; Type: INDEX; Schema: public; Owner: pi
--

CREATE INDEX "fki_ClientID" ON public."Orders" USING btree ("ClientID");


--
-- TOC entry 2917 (class 1259 OID 32982)
-- Name: fki_EmployeID; Type: INDEX; Schema: public; Owner: pi
--

CREATE INDEX "fki_EmployeID" ON public."Orders" USING btree ("EmployeID");


--
-- TOC entry 2932 (class 1259 OID 24836)
-- Name: fki_ProductID; Type: INDEX; Schema: public; Owner: pi
--

CREATE INDEX "fki_ProductID" ON public."ProdOfe" USING btree ("ProductID");


--
-- TOC entry 2933 (class 1259 OID 24845)
-- Name: fki_offerID; Type: INDEX; Schema: public; Owner: pi
--

CREATE INDEX "fki_offerID" ON public."ProdOfe" USING btree ("OfferID");


--
-- TOC entry 2956 (class 2620 OID 24730)
-- Name: Offers set_offer_id; Type: TRIGGER; Schema: public; Owner: pi
--

CREATE TRIGGER set_offer_id BEFORE INSERT ON public."Offers" FOR EACH ROW WHEN ((new."OfferID" IS NULL)) EXECUTE FUNCTION public.generate_offer_id();


--
-- TOC entry 2946 (class 2606 OID 24794)
-- Name: Offers ClienID; Type: FK CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public."Offers"
    ADD CONSTRAINT "ClienID" FOREIGN KEY ("ClientID") REFERENCES public."Clients"("ClientID");


--
-- TOC entry 2940 (class 2606 OID 24799)
-- Name: Orders ClientID; Type: FK CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public."Orders"
    ADD CONSTRAINT "ClientID" FOREIGN KEY ("ClientID") REFERENCES public."Clients"("ClientID") ON UPDATE RESTRICT ON DELETE RESTRICT NOT VALID;


--
-- TOC entry 2942 (class 2606 OID 24897)
-- Name: DeliveryNotes ClientID; Type: FK CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public."DeliveryNotes"
    ADD CONSTRAINT "ClientID" FOREIGN KEY ("ClientID") REFERENCES public."Clients"("ClientID") NOT VALID;


--
-- TOC entry 2944 (class 2606 OID 24939)
-- Name: Invoices ClientID; Type: FK CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public."Invoices"
    ADD CONSTRAINT "ClientID" FOREIGN KEY ("ClientID") REFERENCES public."Clients"("ClientID") NOT VALID;


--
-- TOC entry 2952 (class 2606 OID 24914)
-- Name: ProdDn DeliveryNoteID; Type: FK CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public."ProdDn"
    ADD CONSTRAINT "DeliveryNoteID" FOREIGN KEY ("DeliveryNoteID") REFERENCES public."DeliveryNotes"("DeliveryNoteID") NOT VALID;


--
-- TOC entry 2947 (class 2606 OID 24738)
-- Name: Offers EmployeID; Type: FK CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public."Offers"
    ADD CONSTRAINT "EmployeID" FOREIGN KEY ("EmployeID") REFERENCES public."Employes"("EmployeID") ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- TOC entry 2943 (class 2606 OID 24892)
-- Name: DeliveryNotes EmployeID; Type: FK CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public."DeliveryNotes"
    ADD CONSTRAINT "EmployeID" FOREIGN KEY ("EmployeID") REFERENCES public."Employes"("EmployeID") NOT VALID;


--
-- TOC entry 2945 (class 2606 OID 24944)
-- Name: Invoices EmployeID; Type: FK CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public."Invoices"
    ADD CONSTRAINT "EmployeID" FOREIGN KEY ("EmployeID") REFERENCES public."Employes"("EmployeID") NOT VALID;


--
-- TOC entry 2941 (class 2606 OID 32983)
-- Name: Orders EmployeID; Type: FK CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public."Orders"
    ADD CONSTRAINT "EmployeID" FOREIGN KEY ("EmployeID") REFERENCES public."Employes"("EmployeID") ON UPDATE RESTRICT ON DELETE RESTRICT NOT VALID;


--
-- TOC entry 2954 (class 2606 OID 24962)
-- Name: ProdInv InvoiceID; Type: FK CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public."ProdInv"
    ADD CONSTRAINT "InvoiceID" FOREIGN KEY ("InvoiceID") REFERENCES public."Invoices"("InvoiceID");


--
-- TOC entry 2950 (class 2606 OID 24880)
-- Name: ProdOrd OrderID; Type: FK CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public."ProdOrd"
    ADD CONSTRAINT "OrderID" FOREIGN KEY ("OrderID") REFERENCES public."Orders"("OrderID") NOT VALID;


--
-- TOC entry 2953 (class 2606 OID 24821)
-- Name: ProdDn ProductID; Type: FK CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public."ProdDn"
    ADD CONSTRAINT "ProductID" FOREIGN KEY ("ProductID") REFERENCES public."Products"("ProductID");


--
-- TOC entry 2948 (class 2606 OID 24831)
-- Name: ProdOfe ProductID; Type: FK CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public."ProdOfe"
    ADD CONSTRAINT "ProductID" FOREIGN KEY ("ProductID") REFERENCES public."Products"("ProductID") NOT VALID;


--
-- TOC entry 2951 (class 2606 OID 24875)
-- Name: ProdOrd ProductID; Type: FK CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public."ProdOrd"
    ADD CONSTRAINT "ProductID" FOREIGN KEY ("ProductID") REFERENCES public."Products"("ProductID") NOT VALID;


--
-- TOC entry 2955 (class 2606 OID 24957)
-- Name: ProdInv ProductID; Type: FK CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public."ProdInv"
    ADD CONSTRAINT "ProductID" FOREIGN KEY ("ProductID") REFERENCES public."Products"("ProductID");


--
-- TOC entry 2949 (class 2606 OID 24840)
-- Name: ProdOfe offerID; Type: FK CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public."ProdOfe"
    ADD CONSTRAINT "offerID" FOREIGN KEY ("OfferID") REFERENCES public."Offers"("OfferID") NOT VALID;


--
-- TOC entry 3092 (class 0 OID 0)
-- Dependencies: 4
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: pi
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2025-05-24 16:07:32

--
-- PostgreSQL database dump complete
--

