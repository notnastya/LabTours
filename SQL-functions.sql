
----------очистка таблиц-----------

-- очистка всех таблиц
DROP FUNCTION IF EXISTS clear_all_tables();
CREATE FUNCTION clear_all_tables()
	RETURNS void AS 
	$$ 
	DELETE FROM tour;
	DELETE FROM employee;
	DELETE FROM client;
    DELETE FROM sale;
	$$
	
LANGUAGE sql;


-- очистка таблицы tour
DROP FUNCTION IF EXISTS clear_tour();
CREATE FUNCTION clear_tour()
	RETURNS void AS 
	$$ 
	DELETE FROM tour;
	$$	
LANGUAGE sql;


-- очистка таблицы employee
DROP FUNCTION IF EXISTS clear_employee();
CREATE FUNCTION clear_employee()
	RETURNS void AS 
	$$ 
	DELETE FROM employee;
	$$	
LANGUAGE sql;


-- очистка таблицы client
DROP FUNCTION IF EXISTS clear_client();
CREATE FUNCTION clear_client()
	RETURNS void AS 
	$$ 
	DELETE FROM client;
	$$	
LANGUAGE sql;

-- очистка таблицы sale
DROP FUNCTION IF EXISTS clear_sale();
CREATE FUNCTION clear_sale()
	RETURNS void AS 
	$$ 
	DELETE FROM sale;
	$$	
LANGUAGE sql;


---------вывод таблиц---------

-- вывод таблицы продаж
DROP FUNCTION IF EXISTS show_table_sale();
CREATE FUNCTION show_table_sale()
	RETURNS TABLE (id INTEGER,
                    sale_date DATE,
					employee INTEGER,
					client INTEGER,
					tour INTEGER) 
    AS
	$$
	BEGIN
		IF EXISTS (SELECT * FROM sale) THEN
			RETURN QUERY
				SELECT * FROM sale;
		ELSE
			RAISE NOTICE 'This table is empty';
		END IF;
	END;
	$$
LANGUAGE plpgsql;

-- вывод таблицы туров
DROP FUNCTION IF EXISTS show_table_tour();
CREATE FUNCTION show_table_tour()
	RETURNS TABLE (id INTEGER,
                    price NUMERIC(7,2),
                    departure_date DATE,
					departure_city VARCHAR(40),
					tour_operator VARCHAR(30),
					duration INTEGER,
                    country VARCHAR(40)) AS
	$$
	BEGIN
		IF EXISTS (SELECT * FROM tour) THEN
			RETURN QUERY
				SELECT * FROM tour;
		ELSE
			RAISE NOTICE 'This table is empty';
		END IF;
	END;
	$$
LANGUAGE plpgsql;

-- вывод таблицы работников
DROP FUNCTION IF EXISTS show_table_employee();
CREATE FUNCTION show_table_employee()
	RETURNS TABLE (id INTEGER,
					name VARCHAR(50),
                    phone_number NUMERIC(11,0),
					sales_quantity INTEGER) AS
	$$
	BEGIN
		IF EXISTS (SELECT * FROM employee) THEN
			RETURN QUERY
				SELECT * FROM employee;
		ELSE
			RAISE NOTICE 'Table is empty';
		END IF;
	END;
	$$
LANGUAGE plpgsql;

-- вывод таблицы клиентов
DROP FUNCTION IF EXISTS show_table_client();
CREATE FUNCTION show_table_client()
	RETURNS TABLE (id INTEGER,
					name VARCHAR(50),
                    passport NUMERIC(10,0),
					phone_number NUMERIC(11,0)) AS
	$$
	BEGIN
		IF EXISTS (SELECT * FROM client) THEN
			RETURN QUERY
				SELECT * FROM client;
		ELSE
			RAISE NOTICE 'Table is empty';
		END IF;
	END;
	$$
LANGUAGE plpgsql;


-----------добавление в таблицы-----------

--добавление в таблицу client
DROP FUNCTION IF EXISTS add_to_client(INTEGER, VARCHAR(50),  NUMERIC(10,0), NUMERIC(11,0));
CREATE FUNCTION add_to_client(v_id INTEGER,
					v_name VARCHAR(50),
                    v_passport NUMERIC(10,0),
					v_phone_number NUMERIC(11,0)) -- v означает переменная
	RETURNS INTEGER AS
	$$
	BEGIN 
		IF EXISTS (SELECT c.id FROM client c WHERE c.id = v_id) THEN
			RAISE NOTICE 'Client with id % already exists', v_id;
			RETURN 0;
		ELSE 
			INSERT INTO Client (id, name, passport, phone_number)
			VALUES (v_id, v_name, v_passport, v_phone_number);
			RETURN 1;
		END IF;
	END;
	$$ LANGUAGE plpgsql;


-- добавление в таблицу client
DROP FUNCTION IF EXISTS add_to_employee(INTEGER, VARCHAR(50), NUMERIC(11,0), INTEGER);
CREATE FUNCTION add_to_employee(v_id INTEGER,
					v_name VARCHAR(50),
                    v_phone_number NUMERIC(11,0),
					v_sales_quantity INTEGER)
	RETURNS INTEGER AS
	$$
	BEGIN 
		IF EXISTS (SELECT e.id FROM employee e WHERE e.id = v_id) THEN
			RAISE NOTICE 'Employee with id % already exists', v_id;
			RETURN 0;
		ELSE 
			INSERT INTO Employee (id, name, phone_number, sales_quantity)
			VALUES (v_id, v_name, v_phone_number, v_sales_quantity);
			RETURN 1;
		END IF;
	END;
	$$ LANGUAGE plpgsql;


-- добавление  в таблицу tour
DROP FUNCTION IF EXISTS add_to_tour(INTEGER, NUMERIC(7,2), DATE, VARCHAR(40), VARCHAR(30), INTEGER,  VARCHAR(40));
CREATE FUNCTION add_to_tour(v_id INTEGER,
                    v_price NUMERIC(7,2),
                    v_departure_date DATE,
					v_departure_city VARCHAR(40),
					v_tour_operator VARCHAR(30),
					v_duration INTEGER,
                    v_country VARCHAR(40))
	RETURNS INTEGER AS
	$$
	BEGIN 
		IF EXISTS (SELECT t.id FROM tour t WHERE t.id = v_id) THEN
			RAISE NOTICE 'Tour with id % already exists', v_id;
			RETURN 0;
		ELSE 
			INSERT INTO Tour (id, price, departure_date, departure_city, tour_operator, duration, country)
			VALUES (v_id, v_price, v_departure_date, v_departure_city, v_tour_operator, v_duration, v_country);
			RETURN 1;
		END IF;
	END;
	$$ LANGUAGE plpgsql;


-- добавление в таблицу sale
DROP FUNCTION IF EXISTS add_to_sale(INTEGER, DATE, INTEGER, INTEGER, INTEGER);
CREATE FUNCTION add_to_sale(v_id INTEGER,
                    v_sale_date DATE,
					v_employee INTEGER,
					v_client INTEGER,
					v_tour INTEGER)
	RETURNS INTEGER AS
	$$
	BEGIN 
		IF NOT EXISTS (SELECT c.id FROM client c WHERE c.id = v_client) THEN
			RAISE NOTICE 'Client % does not exist', v_client;
			RETURN 0;
		
		ELSIF NOT EXISTS (SELECT e.id FROM employee e WHERE e.id = v_employee) THEN
			RAISE NOTICE 'Employee % does not exist', v_employee;
			RETURN 0;
		ELSIF NOT EXISTS (SELECT t.id FROM tour t WHERE t.id = v_tour) THEN
			RAISE NOTICE 'Tour % does not exist', v_tour;
			RETURN 0;							  
		ELSIF EXISTS (SELECT s.id FROM sale s WHERE s.id = v_id) THEN
			RAISE NOTICE 'Sale with id % already exists', v_id;
			RETURN 0;
		ELSE
			INSERT INTO sale (id , sale_date, employee, client, tour)
			VALUES (v_id , v_sale_date , v_employee , v_client , v_tour );
			RETURN 1;
		END IF;
	END;
$$ LANGUAGE plpgsql;



-----------поиск по таблице------------

-- поиск клиента по имени
DROP FUNCTION IF EXISTS search_client_by_name(VARCHAR(50));
CREATE FUNCTION search_client_by_name(v_name VARCHAR(50))
	RETURNS TABLE (id INTEGER,
					name VARCHAR(50),
                    passport NUMERIC(10,0),
					phone_number NUMERIC(11,0)) AS
	$$
	BEGIN 
		IF EXISTS (SELECT c.name FROM client c WHERE c.name = v_name) THEN
			RETURN QUERY
				SELECT * FROM client c
				WHERE c.name = v_name;
		ELSE 
			RAISE NOTICE 'Client with name % does not exist', v_name;
		END IF;
	END;
	$$
LANGUAGE plpgsql;

--поиск продажи по айди
DROP FUNCTION IF EXISTS search_sale_by_id(INTEGER);
CREATE FUNCTION search_sale_by_id(v_id INTEGER)
	RETURNS TABLE (id INTEGER,
                    sale_date DATE,
					employee INTEGER,
					client INTEGER,
					tour INTEGER) 
					AS
	$$
	BEGIN 
		IF EXISTS (SELECT s.id FROM sale s WHERE s.id = v_id) THEN
			RETURN QUERY
				SELECT * FROM sale s
				WHERE s.id = v_id;
		ELSE 
			RAISE NOTICE 'Sale with id % does not exist', v_id;
		END IF;
	END;
	$$
LANGUAGE plpgsql;

--поиск тура по айди
DROP FUNCTION IF EXISTS search_tour_by_id(INTEGER);
CREATE FUNCTION search_tour_by_id(v_id INTEGER)
	RETURNS TABLE (id INTEGER,
                    price NUMERIC(7,2),
                    departure_date DATE,
					departure_city VARCHAR(40),
					tour_operator VARCHAR(30),
					duration INTEGER,
                    country VARCHAR(40))
					AS
	$$
	BEGIN 
		IF EXISTS (SELECT t.id FROM tour t WHERE t.id = v_id) THEN
			RETURN QUERY
				SELECT * FROM tour t
				WHERE t.id = v_id;
		ELSE 
			RAISE NOTICE 'Tour with id % does not exist', v_id;
		END IF;
	END;
	$$
LANGUAGE plpgsql;

--поиск тура по названию страны
DROP FUNCTION IF EXISTS search_tour_by_country(VARCHAR(40));
CREATE FUNCTION search_tour_by_country(v_country VARCHAR(40))
	RETURNS TABLE (id INTEGER,
                    price NUMERIC(7,2),
                    departure_date DATE,
					departure_city VARCHAR(40),
					tour_operator VARCHAR(30),
					duration INTEGER,
                    country VARCHAR(40))
					AS
	$$
	BEGIN 
		IF EXISTS (SELECT t.country FROM tour t WHERE t.country = v_country) THEN
			RETURN QUERY
				SELECT * FROM tour t
				WHERE t.country = v_country;
		ELSE 
			RAISE NOTICE 'Tour with country % does not exist', v_country;
		END IF;
	END;
	$$
LANGUAGE plpgsql;

----поиск работника по айди
DROP FUNCTION IF EXISTS search_employee_by_id(INTEGER);
CREATE FUNCTION search_employee_by_id(v_id INTEGER)
	RETURNS TABLE (id INTEGER,
					name VARCHAR(50),
                    phone_number NUMERIC(11,0),
					sales_quantity INTEGER)
					AS
	$$
	BEGIN 
		IF EXISTS (SELECT e.id FROM employee e WHERE e.id = v_id) THEN
			RETURN QUERY
				SELECT * FROM employee e
				WHERE e.id = v_id;
		ELSE 
			RAISE NOTICE 'Employee with id % does not exist', v_id;
		END IF;
	END;
	$$
LANGUAGE plpgsql;

-- поиск работника по имени
DROP FUNCTION IF EXISTS search_employee_by_name(VARCHAR(50));
CREATE FUNCTION search_employee_by_name(v_name VARCHAR(50))
	RETURNS TABLE (id INTEGER,
					name VARCHAR(50),
                    phone_number NUMERIC(11,0),
					sales_quantity INTEGER) AS
	$$
	BEGIN 
		IF EXISTS (SELECT e.name FROM employee e WHERE e.name = v_name) THEN
			RETURN QUERY
				SELECT * FROM employee e 
				WHERE e.name = v_name;
		ELSE 
			RAISE NOTICE 'Employee with name % does not exist', v_name;
		END IF;
	END;
	$$
LANGUAGE plpgsql;


-------удаление из таблиц------

-- удаление клиента по имени
DROP FUNCTION IF EXISTS delete_client_by_name(VARCHAR(50));
CREATE FUNCTION delete_client_by_name(v_name VARCHAR(50))
	RETURNS INTEGER AS
	$$
	BEGIN 
		IF EXISTS (SELECT c.name FROM client c WHERE c.name = v_name) THEN
			DELETE FROM client c
			WHERE c.name = v_name;
			RETURN 1;
		ELSE 
			RAISE NOTICE 'Client with name % does not exist', v_name;
			RETURN 0;
		END IF;
	END;
	$$
LANGUAGE plpgsql;

-- удаление клиента по айди
DROP FUNCTION IF EXISTS delete_client_by_id(INTEGER);
CREATE FUNCTION delete_client_by_id(v_id INTEGER)
	RETURNS INTEGER AS
	$$
	BEGIN 
		IF EXISTS (SELECT c.id FROM client c WHERE c.id = v_id) THEN
			DELETE FROM client c
			WHERE c.id = v_id;
			RETURN 1;
		ELSE 
			RAISE NOTICE 'Client with id % does not exist', in_id;
			RETURN 0;
		END IF;
	END;
	$$
LANGUAGE plpgsql;


-- удаление тура по айди
DROP FUNCTION IF EXISTS delete_tour_by_id(INTEGER);
CREATE FUNCTION delete_tour_by_id(v_id INTEGER)
	RETURNS INTEGER AS
	$$
	BEGIN 
		IF EXISTS (SELECT t.id FROM tour t WHERE t.id = v_id) THEN
			DELETE FROM tour t
			WHERE t.id = v_id;
			RETURN 1;
		ELSE 
			RAISE NOTICE 'Tour with id % does not exist', v_id;
			RETURN 0;
		END IF;
	END;
	$$
LANGUAGE plpgsql;


-- удаление работника по айди
DROP FUNCTION IF EXISTS delete_employee_by_id(INTEGER);
CREATE FUNCTION delete_employee_by_id(v_id INTEGER)
	RETURNS INTEGER AS
	$$
	BEGIN 
		IF EXISTS (SELECT e.id FROM employee e WHERE e.id = v_id) THEN
			DELETE FROM employee e
			WHERE e.id = v_id;
			RETURN 1;
		ELSE 
			RAISE NOTICE 'Employee with id % does not exist', v_id;
			RETURN 0;
		END IF;
	END;
	$$
LANGUAGE plpgsql;

-- удаление работника по имени
DROP FUNCTION IF EXISTS delete_employee_by_name(VARCHAR(50));
CREATE FUNCTION delete_employee_by_name(v_name VARCHAR(50))
	RETURNS INTEGER AS
	$$
	BEGIN 
		IF EXISTS (SELECT e.name FROM employee e WHERE e.name = v_name) THEN
			DELETE FROM employee e
			WHERE e.name = v_name;
			RETURN 1;
		ELSE 
			RAISE NOTICE 'Employee with name % does not exist', v_id;
			RETURN 0;
		END IF;
	END;
	$$
LANGUAGE plpgsql;


-- удаление продажи по айди
DROP FUNCTION IF EXISTS delete_sale_by_id(INTEGER);
CREATE FUNCTION delete_sale_by_id(v_id INTEGER)
	RETURNS INTEGER AS
	$$
	BEGIN 
		IF EXISTS (SELECT s.id FROM sale s WHERE s.id = v_id) THEN
			DELETE FROM sale s
			WHERE s.id = v_id;
			RETURN 1;
		ELSE 
			RAISE NOTICE 'Sale with id % does not exist', v_id;
			RETURN 0;
		END IF;
	END;
	$$
LANGUAGE plpgsql;

------обновление таблицы----------


-- обновление записи в таблице tour по id 
-- если на вход вместо числа подается -1 или если вместо строки подается '', этот аттрибут остается без изменения
-- начение даты по умолчанию: 1970-01-01

--обновление тура
DROP FUNCTION IF EXISTS update_tour(INTEGER, NUMERIC(7,2), DATE, VARCHAR(40), VARCHAR(30), INTEGER, VARCHAR(40));
CREATE FUNCTION update_tour(v_id INTEGER,
                    v_price NUMERIC(7,2),
                    v_departure_date DATE,
					v_departure_city VARCHAR(40),
					v_tour_operator VARCHAR(30),
					v_duration INTEGER,
                    v_country VARCHAR(40))
	RETURNS INTEGER AS
	$$
	BEGIN 
		IF EXISTS (SELECT t.id FROM tour t WHERE t.id = v_id) THEN
			IF (v_price <> -1) THEN
					UPDATE tour t
					SET price = v_price
					WHERE id = v_id;
			END IF;
			IF (v_departure_date <> '1970-01-01') THEN 
					UPDATE tour t
					SET departure_date = v_departure_date
					WHERE id = v_id;
			END IF;
			IF (v_departure_city <> '') THEN 
				UPDATE tour t
				SET departure_city = v_departure_city
				WHERE id = v_id;
			END IF;	
			IF (v_tour_operator <> '') THEN 
				UPDATE tour t
				SET tour_operator = v_tour_operator
				WHERE id = v_id;
			END IF;
			IF (v_duration <> -1) THEN 
				UPDATE tour t
				SET duration = v_duration
				WHERE id = v_id;
			END IF;
			IF (v_country <> '') THEN 
				UPDATE tour t
				SET country = v_country
				WHERE id = v_id;
			END IF;		
			RETURN 1;	
		ELSE 
			RAISE NOTICE 'Tour with id % does not exist', v_id;
			RETURN 0;
		END IF;
	END;
	$$
LANGUAGE plpgsql;
