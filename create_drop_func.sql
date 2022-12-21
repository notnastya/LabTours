CREATE EXTENSION IF NOT EXISTS dblink;

--создание базы данных

CREATE OR REPLACE FUNCTION create_db(dbname text, username text )
	RETURNS INTEGER AS
	$func$
	BEGIN
		IF EXISTS (SELECT datname FROM pg_database WHERE datname = dbname) THEN
   			RAISE NOTICE 'Database already exists';
			RETURN 0; 
		ELSE
   			PERFORM dblink_exec('user=db_creator password=db_creator dbname=' || current_database(),
								'CREATE DATABASE ' || dbname); 
								
			PERFORM dblink_exec('user=db_creator password=db_creator dbname=' || dbname,
			'
			DROP TABLE IF EXISTS tour CASCADE;
				CREATE TABLE tour(
					id INTEGER NOT NULL UNIQUE,
                    price NUMERIC(7,2) CHECK (price > 0),
                    departure_date DATE NOT NULL,
					departure_city VARCHAR(40) NOT NULL,
					tour_operator VARCHAR(30) NOT NULL,
					duration INTEGER NOT NULL CHECK (duration > 0),
                    country VARCHAR(40) NOT NULL,
					PRIMARY KEY (id)
				);
				DROP TABLE IF EXISTS employee CASCADE;
				CREATE TABLE employee(
					id INTEGER NOT NULL UNIQUE,
					name VARCHAR(50) NOT NULL,
                    phone_number NUMERIC(11,0) NOT NULL,
					sales_quantity INTEGER DEFAULT 0 CHECK (sales_quantity >= 0),
					PRIMARY KEY (id)
				);
                DROP TABLE IF EXISTS client CASCADE;
				CREATE TABLE client(
					id INTEGER NOT NULL UNIQUE,
					name VARCHAR(50) NOT NULL,
                    passport NUMERIC(10,0) NOT NULL,
					phone_number NUMERIC(11,0) NOT NULL,
					PRIMARY KEY (id)
				);
				DROP TABLE IF EXISTS sale CASCADE;
				CREATE TABLE sale(
					id INTEGER NOT NULL UNIQUE,
                    sale_date DATE NOT NULL,
					employee INTEGER NOT NULL,
					client INTEGER NOT NULL,
					tour INTEGER NOT NULL,
					PRIMARY KEY (id),
                    FOREIGN KEY (tour) REFERENCES Tour(id) ON DELETE CASCADE,
					FOREIGN KEY (client) REFERENCES Client(id) ON DELETE CASCADE,
					FOREIGN KEY (employee) REFERENCES Employee(id) ON DELETE CASCADE

				);

				CREATE INDEX name_index ON client (name);
				CREATE INDEX name_index_emp ON employee (name);

			'

			);

			PERFORM dblink_exec('user=db_creator password=db_creator dbname=' || dbname,
			'GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ' || username );
			RETURN 1;
		END IF;

	END
	$func$ 
	LANGUAGE plpgsql;

--удаление базы данных

DROP FUNCTION IF EXISTS drop_db(text);
CREATE FUNCTION drop_db(dbname text)
	RETURNS INTEGER AS
	$func$
	BEGIN
		IF EXISTS (SELECT datname FROM pg_database WHERE datname = dbname) THEN
   			PERFORM dblink_exec('user=db_creator password=db_creator dbname=' || current_database(), 
								'DROP DATABASE ' || quote_ident(dbname));
			RETURN 1;			
		ELSE
			RAISE NOTICE 'Database does not exist';
			RETURN 0; 
		END IF;

	END
	$func$ 
	LANGUAGE plpgsql;
