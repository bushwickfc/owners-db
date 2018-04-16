START TRANSACTION;
create table owner_type (
  owner_type varchar(20) NOT NULL,
  display_name varchar(255) NOT NULL,
  description varchar(255),
  work_requirement int NOT NULL,
  work_surrogate int NOT NULL,
  shopping_surrogate int NOT NULL,
  owner_price bit(1) NOT NULL,
  created_at timestamp DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY(owner_type)
);

create table owner (
  owner_id int AUTO_INCREMENT,
  old_member_id int,
  pos_id varchar(255),
  seven_shifts_id varchar(255),
  status varchar(20) NOT NULL,
  owner_type varchar(20) NOT NULL,
  email varchar(254) NOT NULL,
  first_name text NOT NULL,
  last_name text NOT NULL,
  display_name text,
  join_date date NOT NULL,
  phone varchar(10),
  address text,
  city text,
  country text,
  zipcode varchar(9),
  created_at timestamp DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (owner_id),
  FOREIGN KEY (owner_type)
  REFERENCES owner_type(owner_type)
  ON UPDATE CASCADE,
  FOREIGN KEY(status)
  REFERENCES status(status)
  ON UPDATE CASCADE
);

create table owner_owner_type_history (
  owner_id int NOT NULL,
  owner_type varchar(20) NOT NULL,
  start_date date NOT NULL,
  end_date date,
  created_at timestamp DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY(owner_id, start_date),
  FOREIGN KEY (owner_type)
  REFERENCES owner_type(owner_type)
  ON UPDATE CASCADE,
  FOREIGN KEY (owner_id)
  REFERENCES owner(owner_id)
  ON UPDATE CASCADE
);

create table household (
  household varchar(255),
  owner_id int,
  PRIMARY KEY (household, owner_id),
  FOREIGN KEY (owner_id)
  REFERENCES owner(owner_id)
  ON UPDATE CASCADE
);

create table hour_reason (
  hour_reason varchar(20) NOT NULL,
  display_name varchar(255) NOT NULL,
  description varchar(255),
  created_at timestamp DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY(hour_reason)
);

create table hour_log (
  owner_id int NOT NULL,
  amount int NOT NULL,
  hour_reason varchar(20) NOT NULL,
  hour_date date NOT NULL,
  created_at timestamp DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY(owner_id, hour_reason, hour_date),
  FOREIGN KEY(hour_reason)
  REFERENCES hour_reason(hour_reason)
  ON UPDATE CASCADE,
  FOREIGN KEY(owner_id)
  REFERENCES owner(owner_id)
  ON UPDATE CASCADE
);

create table equity_round (
  equity_round varchar(20) NOT NULL,
  display_name varchar(255) NOT NULL,
  description varchar(255),
  created_at timestamp DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY(equity_round)
);

create table equity_type (
  equity_round varchar(20) NOT NULL,
  equity_type varchar(20) NOT NULL,
  amount DECIMAL(10,2) NOT NULL,
  payment_plan_amount DECIMAL(10,2) NOT NULL,
  display_name varchar(255) NOT NULL,
  description varchar(255),
  created_at timestamp DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY(equity_type),
  FOREIGN KEY(equity_round)
  REFERENCES equity_round(equity_round)
  ON UPDATE CASCADE
);

create table owner_equity_type (
  owner_id int NOT NULL,
  equity_type varchar(20) NOT NULL,
  payment_plan bit(1) NOT NULL,
  created_at timestamp DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY(owner_id, equity_type),
  FOREIGN KEY(equity_type)
  REFERENCES equity_type(equity_type)
  ON UPDATE CASCADE
);

create table equity_log (
  owner_id int NOT NULL,
  amount DECIMAL(10,2) NOT NULL,
  transaction_date date NOT NULL,
  created_at timestamp DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY(owner_id, transaction_date),
  FOREIGN KEY(owner_id)
  REFERENCES owner(owner_id)
  ON UPDATE CASCADE
);
COMMIT;
