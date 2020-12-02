-- Second schema update

-- Create TriggerDefinition and TriggerInstance
-- TriggerDefinition.className should be unique
-- Index TriggerInstance by playerId

ALTER TABLE DepartureEvent ADD COLUMN finalDestinationId bigint unsigned /* Star */;

create table TriggerDefinition (
    triggerDefinitionId            int not null primary key auto_increment,
	className                      varchar(255)
);

create table TriggerInstance (
    triggerInstanceId              int not null primary key auto_increment,
	triggerDefId                   bigint unsigned /* TriggerDefinition */ not null,
	playerId                       bigint unsigned /* Player */ not null,
	userFieldValues                text,
	messageTransport               varchar(64) not null,
	gameId                         bigint unsigned /* Game */ not null
);

CREATE UNIQUE INDEX TriggerDefinition_className ON TriggerDefinition(className);
CREATE INDEX TriggerInstance_playerId ON TriggerInstance(playerId);

