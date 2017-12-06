CREATE TABLE user {
	username varchar(20),
    password varchar(50),
    fname varchar(20),
    lname varchar(20),
    PRIMARY KEY (username)
};

CREATE TABLE Content {
	ID int(8),
	date Date(8),
	file_path varchar(50),
    name varchar(20),    
	is_pub Boolean,
	PRIMARY KEY (ID)
};

CREATE TABLE FriendGroup {
	name varchar(20),
	description varchar(120),
	username varchar(20),
	PRIMARY KEY(name, username)
    FOREIGN KEY username references Person(username)
};

CREATE TABLE comment {
	username varchar(20),
	ID int(8),
	timestamp Timestamp(100),
	text varchar(120),
	PRIMARY KEY(timestamp, ID, username)
    FOREIGN KEY ID references Person(ID)
    FOREIGN KEY username references Person(username)
};

CREATE TABLE share {
	name varchar(20),
	ID int(8),
	owner varchar(20),
	PRIMARY KEY (name, ID, owner)
    FOREIGN KEY (name, owner) references FriendGroup(name, username)
    FOREIGN KEY ID references Content(ID)
};

CREATE TABLE comment_by {
	timestamp Timestamp(100)
	ID int (8),
	username varchar(20),
	owner varchar(20),
	PRIMARY KEY (timestamp, username)
    FOREIGN KEY (timestamp, ID, owner) references Comment (timestamp, ID, username)
    FOREIGN KEY username references Person(username)
};

CREATE TABLE comment_on {
	timestamp Timestamp(100),
	ID int(8),
	owner_id int(8),
	owner varchar(20),
	PRIMARY KEY (timestamp, ID)
    FOREIGN KEY (timestamp, owner_id, owner) references Comment(timestamp, ID, username)
    FOREIGN KEY ID references Content(ID)
};

CREATE TABLE member_of {
	username varchar(20),
	name varchar(20),
	owner varchar(20),
	PRIMARY KEY (username, name)
    FOREIGN KEY username references Person (username)
    FOREIGN KEY (name, owner) references FriendGroup(name, username)
};

CREATE TABLE Post {
	username varchar(20),
	ID int(8),
	PRIMARY KEY (username, ID)
    FOREIGN KEY username references Person(username)
    FOREIGN KEY ID references Content(ID)
};

CREATE TABLE Tag {
	timestamp Timestamp(100),
	is_pub BOOLEAN,
	ID int(8),
	tagger varchar(20), 
	taggee varchar(20),
	PRIMARY KEY (ID, tagger, taggee)
    FOREIGN KEY ID references Content(ID)
    FOREIGN KEY tagger references Person(username)
    FOREIGN KEY taggee references Person(username)
};

