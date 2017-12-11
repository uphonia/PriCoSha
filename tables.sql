CREATE TABLE user {
	username varchar(20),
    password varchar(50),
    fname varchar(20),
    lname varchar(20),
    PRIMARY KEY (username)
};

CREATE TABLE Content {
	ID int(8),
	timestamp Timestamp(6),
	link varchar(50),
    name varchar(20),    
	privacy Boolean,
	username varchar(20),
	PRIMARY KEY (ID)
	FOREIGN KEY username references user(username)
};

CREATE TABLE FriendGroup {
	name varchar(20),
	description varchar(120),
	username varchar(20),
	PRIMARY KEY(name, username)
    FOREIGN KEY username references user(username)
};

CREATE TABLE member_of {
	username varchar(20),
	name varchar(20),
	owner varchar(20),
	PRIMARY KEY (username, name)
    FOREIGN KEY username references user(username)
    FOREIGN KEY (name, owner) references FriendGroup(name, username)
};

CREATE TABLE comment {
	username varchar(20),
	timestamp Timestamp(100),
	text varchar(120),
	ID int(8)
	PRIMARY KEY(timestamp, username, ID)
    FOREIGN KEY username references user(username)
    FOREIGN KEY ID references Content(ID)
};

CREATE TABLE Share {
	name varchar(20),
	ID int(8),
	owner varchar(20),
	PRIMARY KEY (name, ID, owner)
    FOREIGN KEY (name, owner) references FriendGroup(name, username)
    FOREIGN KEY ID references Content(ID)
};

CREATE TABLE Post {
	username varchar(20),
	ID int(8),
	PRIMARY KEY (username, ID)
    FOREIGN KEY username references user(username)
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
    FOREIGN KEY tagger references user(username)
    FOREIGN KEY taggee references user(username)
};

