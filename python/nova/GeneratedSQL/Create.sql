/*
Start of generated SQL.

# Date         = Tue Mar 29 11:44:59 2005
# Python ver   = 2.4 (#60, Nov 30 2004, 11:49:19) [MSC v.1310 32 bit (Intel)]
# Op Sys       = nt
# Platform     = win32
# Cur dir      = C:\home\kgilpin\nova\python\nova
# Num classes  = 29

Classes:
	GlobalLock
	Game
	User
	GameObject
	Player
	Star
	StandingOrder
	Garrison
	Routing
	Event
	DepartureEvent
	ArrivalEvent
	PurchaseEvent
	PurchaseFactoriesEvent
	PurchaseSpeedEvent
	PurchaseRangeEvent
	PurchaseBattlePowerEvent
	PurchaseProbeShieldEvent
	PurchaseDeathShieldEvent
	CreateRoutingEvent
	RemoveRoutingEvent
	BattleEvent
	GlobalProductionEvent
	ProductionEvent
	SpyProbeEvent
	DeathProbeEvent
	FieryDeathEvent
	TriggerDefinition
	TriggerInstance
*/

--drop database if exists nova;
--create database nova;
use nova;

create table GlobalLock (
    globalLockId                   int not null primary key auto_increment,
	dummyAttr                      int
);


create table Game (
    gameId                         int not null primary key auto_increment,
	timeCompression                double precision default 1,
	lastActionTime                 datetime,
	eventCounter                   int default 0,
	startTime                      datetime not null,
	endTime                        datetime not null,
	deathProbeCost                 int not null default 200,
	spyProbeCost                   int not null default 10,
	factoryCost                    int not null default 5,
	speedCost                      int not null default 500,
	battlePowerCost                int not null default 100,
	rangeCost                      int not null default 100,
	probeShieldCost                int not null default 10,
	deathShieldCost                int not null default 200,
	name                           varchar(255)
);


create table User (
    userId                         int not null primary key auto_increment,
	name                           varchar(100) /* WARNING: NO LENGTH SPECIFIED */ not null,
	password                       varchar(100) /* WARNING: NO LENGTH SPECIFIED */ not null,
	email                          varchar(100) /* WARNING: NO LENGTH SPECIFIED */ not null
);


create table Player (
    playerId                       int not null primary key auto_increment,
	gameId                         bigint unsigned /* Game */ not null,
	userId                         bigint unsigned /* User */ not null,
	name                           varchar(64) not null,
	wealth                         int not null default 250,
	battlePower                    int not null default 100,
	range                          double precision not null default 10,
	speed                          double precision not null default 0.5
);


create table Star (
    starId                         int not null primary key auto_increment,
	gameId                         bigint unsigned /* Game */ not null,
	name                           varchar(64) not null,
	x                              int not null,
	y                              int not null,
	wealth                         int not null default 10,
	numShips                       int not null default 0,
	numFactories                   int not null default 0,
	hasSpyShield                   bool not null default 0,
	hasDeathShield                 bool not null default 0,
	ownerId                        bigint unsigned /* Player */,
	homeWorldOfId                  bigint unsigned /* Player */,
	isDead                         bool not null default 0
	/* standingOrders list of StandingOrder - not a SQL column */
);


create table Garrison (
    garrisonId                     int not null primary key auto_increment,
	gameId                         bigint unsigned /* Game */ not null,
	starId                         bigint unsigned /* Star */ not null,
	numShips                       int not null
);


create table Routing (
    routingId                      int not null primary key auto_increment,
	gameId                         bigint unsigned /* Game */ not null,
	starId                         bigint unsigned /* Star */ not null,
	numShips                       int default 0,
	percent                        double precision default 0,
	destinationId                  bigint unsigned /* Star */
);


create table DepartureEvent (
    departureEventId               int not null primary key auto_increment,
	gameId                         bigint unsigned /* Game */ not null,
	executionTime                  datetime not null,
	eventCounter                   int default -1,
	playerId                       bigint unsigned /* Player */ not null,
	status                         enum("Pending", "InProcess", "Complete", "Invalid", "Aborted") not null default 'Pending',
	numShips                       int not null,
	originId                       bigint unsigned /* Star */ not null,
	destinationId                  bigint unsigned /* Star */ not null,
	arrivalTime                    datetime,
	unitType                       enum("Ship", "SpyProbe", "DeathProbe") not null,
	finalDestinationId             bigint unsigned /* Star */
);


create table ArrivalEvent (
    arrivalEventId                 int not null primary key auto_increment,
	gameId                         bigint unsigned /* Game */ not null,
	executionTime                  datetime not null,
	eventCounter                   int default -1,
	playerId                       bigint unsigned /* Player */ not null,
	status                         enum("Pending", "InProcess", "Complete", "Invalid", "Aborted") not null default 'Pending',
	departureEventId               bigint unsigned /* DepartureEvent */ not null
);


create table PurchaseFactoriesEvent (
    purchaseFactoriesEventId       int not null primary key auto_increment,
	gameId                         bigint unsigned /* Game */ not null,
	executionTime                  datetime not null,
	eventCounter                   int default -1,
	playerId                       bigint unsigned /* Player */ not null,
	status                         enum("Pending", "InProcess", "Complete", "Invalid", "Aborted") not null default 'Pending',
	cost                           double precision not null,
	starId                         bigint unsigned /* Star */ not null,
	delta                          int not null
);


create table PurchaseSpeedEvent (
    purchaseSpeedEventId           int not null primary key auto_increment,
	gameId                         bigint unsigned /* Game */ not null,
	executionTime                  datetime not null,
	eventCounter                   int default -1,
	playerId                       bigint unsigned /* Player */ not null,
	status                         enum("Pending", "InProcess", "Complete", "Invalid", "Aborted") not null default 'Pending',
	cost                           double precision not null,
	delta                          double precision not null
);


create table PurchaseRangeEvent (
    purchaseRangeEventId           int not null primary key auto_increment,
	gameId                         bigint unsigned /* Game */ not null,
	executionTime                  datetime not null,
	eventCounter                   int default -1,
	playerId                       bigint unsigned /* Player */ not null,
	status                         enum("Pending", "InProcess", "Complete", "Invalid", "Aborted") not null default 'Pending',
	cost                           double precision not null,
	delta                          double precision not null
);


create table PurchaseBattlePowerEvent (
    purchaseBattlePowerEventId     int not null primary key auto_increment,
	gameId                         bigint unsigned /* Game */ not null,
	executionTime                  datetime not null,
	eventCounter                   int default -1,
	playerId                       bigint unsigned /* Player */ not null,
	status                         enum("Pending", "InProcess", "Complete", "Invalid", "Aborted") not null default 'Pending',
	cost                           double precision not null,
	delta                          double precision not null
);


create table PurchaseProbeShieldEvent (
    purchaseProbeShieldEventId     int not null primary key auto_increment,
	gameId                         bigint unsigned /* Game */ not null,
	executionTime                  datetime not null,
	eventCounter                   int default -1,
	playerId                       bigint unsigned /* Player */ not null,
	status                         enum("Pending", "InProcess", "Complete", "Invalid", "Aborted") not null default 'Pending',
	cost                           double precision not null,
	starId                         bigint unsigned /* Star */ not null
);


create table PurchaseDeathShieldEvent (
    purchaseDeathShieldEventId     int not null primary key auto_increment,
	gameId                         bigint unsigned /* Game */ not null,
	executionTime                  datetime not null,
	eventCounter                   int default -1,
	playerId                       bigint unsigned /* Player */ not null,
	status                         enum("Pending", "InProcess", "Complete", "Invalid", "Aborted") not null default 'Pending',
	cost                           double precision not null,
	starId                         bigint unsigned /* Star */ not null
);


create table CreateRoutingEvent (
    createRoutingEventId           int not null primary key auto_increment,
	gameId                         bigint unsigned /* Game */ not null,
	executionTime                  datetime not null,
	eventCounter                   int default -1,
	playerId                       bigint unsigned /* Player */ not null,
	status                         enum("Pending", "InProcess", "Complete", "Invalid", "Aborted") not null default 'Pending',
	originId                       bigint unsigned /* Star */ not null,
	destinationId                  bigint unsigned /* Star */ not null,
	garrison                       int not null
);


create table RemoveRoutingEvent (
    removeRoutingEventId           int not null primary key auto_increment,
	gameId                         bigint unsigned /* Game */ not null,
	executionTime                  datetime not null,
	eventCounter                   int default -1,
	playerId                       bigint unsigned /* Player */ not null,
	status                         enum("Pending", "InProcess", "Complete", "Invalid", "Aborted") not null default 'Pending',
	originId                       bigint unsigned /* Star */ not null
);


create table BattleEvent (
    battleEventId                  int not null primary key auto_increment,
	gameId                         bigint unsigned /* Game */ not null,
	executionTime                  datetime not null,
	eventCounter                   int default -1,
	playerId                       bigint unsigned /* Player */ not null,
	status                         enum("Pending", "InProcess", "Complete", "Invalid", "Aborted") not null default 'Pending',
	starId                         bigint unsigned /* Star */ not null,
	attackerId                     bigint unsigned /* Player */ not null,
	defenderId                     bigint unsigned /* Player */ not null,
	victorId                       bigint unsigned /* Player */ not null,
	numAttackingShips              int not null,
	numDefendingShips              int not null,
	numShipsLost                   int not null
);


create table GlobalProductionEvent (
    globalProductionEventId        int not null primary key auto_increment,
	gameId                         bigint unsigned /* Game */ not null,
	executionTime                  datetime not null,
	eventCounter                   int default -1,
	playerId                       bigint unsigned /* Player */ not null,
	status                         enum("Pending", "InProcess", "Complete", "Invalid", "Aborted") not null default 'Pending'
);


create table ProductionEvent (
    productionEventId              int not null primary key auto_increment,
	gameId                         bigint unsigned /* Game */ not null,
	executionTime                  datetime not null,
	eventCounter                   int default -1,
	playerId                       bigint unsigned /* Player */ not null,
	status                         enum("Pending", "InProcess", "Complete", "Invalid", "Aborted") not null default 'Pending',
	starId                         bigint unsigned /* Star */ not null,
	numShips                       int not null,
	wealth                         int not null,
	globalProductionEventId        bigint unsigned /* GlobalProductionEvent */ not null
);


create table SpyProbeEvent (
    spyProbeEventId                int not null primary key auto_increment,
	gameId                         bigint unsigned /* Game */ not null,
	executionTime                  datetime not null,
	eventCounter                   int default -1,
	playerId                       bigint unsigned /* Player */ not null,
	status                         enum("Pending", "InProcess", "Complete", "Invalid", "Aborted") not null default 'Pending',
	starId                         bigint unsigned /* Star */ not null,
	ownerId                        bigint unsigned /* Player */ not null,
	wealth                         int default 0,
	numShips                       int default 0,
	numFactories                   int default 0,
	hasSpyShield                   bool,
	hasDeathShield                 bool default 0
);


create table DeathProbeEvent (
    deathProbeEventId              int not null primary key auto_increment,
	gameId                         bigint unsigned /* Game */ not null,
	executionTime                  datetime not null,
	eventCounter                   int default -1,
	playerId                       bigint unsigned /* Player */ not null,
	status                         enum("Pending", "InProcess", "Complete", "Invalid", "Aborted") not null default 'Pending',
	starId                         bigint unsigned /* Star */ not null,
	hasDeathShield                 bool
);


create table FieryDeathEvent (
    fieryDeathEventId              int not null primary key auto_increment,
	gameId                         bigint unsigned /* Game */ not null,
	executionTime                  datetime not null,
	eventCounter                   int default -1,
	playerId                       bigint unsigned /* Player */ not null,
	status                         enum("Pending", "InProcess", "Complete", "Invalid", "Aborted") not null default 'Pending',
	departureEventId               bigint unsigned /* DepartureEvent */ not null
);


create table TriggerDefinition (
    triggerDefinitionId            int not null primary key auto_increment,
	className                      varchar(100) /* WARNING: NO LENGTH SPECIFIED */ not null
);


create table TriggerInstance (
    triggerInstanceId              int not null primary key auto_increment,
	triggerDefId                   bigint unsigned /* TriggerDefinition */ not null,
	playerId                       bigint unsigned /* Player */ not null,
	userFieldValues                text,
	messageTransport               varchar(64) not null,
	gameId                         bigint unsigned /* Game */ not null
);


create table _MKClassIds (
	id int not null primary key,
	name varchar(100)
);
insert into _MKClassIds (id, name) values
	(1, 'GlobalLock'),
	(2, 'Game'),
	(3, 'User'),
	(4, 'GameObject'),
	(5, 'Player'),
	(6, 'Star'),
	(7, 'StandingOrder'),
	(8, 'Garrison'),
	(9, 'Routing'),
	(10, 'Event'),
	(11, 'DepartureEvent'),
	(12, 'ArrivalEvent'),
	(13, 'PurchaseEvent'),
	(14, 'PurchaseFactoriesEvent'),
	(15, 'PurchaseSpeedEvent'),
	(16, 'PurchaseRangeEvent'),
	(17, 'PurchaseBattlePowerEvent'),
	(18, 'PurchaseProbeShieldEvent'),
	(19, 'PurchaseDeathShieldEvent'),
	(20, 'CreateRoutingEvent'),
	(21, 'RemoveRoutingEvent'),
	(22, 'BattleEvent'),
	(23, 'GlobalProductionEvent'),
	(24, 'ProductionEvent'),
	(25, 'SpyProbeEvent'),
	(26, 'DeathProbeEvent'),
	(27, 'FieryDeathEvent'),
	(28, 'TriggerDefinition'),
	(29, 'TriggerInstance');

show tables

/* end of generated SQL */
