
-- First schema update

-- Index the ProductionEvents by their GlobalProductionEvent
-- Adds a reference from each ProductionEvent back to the GlobalProductionEvent that spawned it
-- Changes the default cost of Speed from 100 to 500

ALTER TABLE ProductionEvent ADD COLUMN globalProductionEventId bigint unsigned /* GlobalProductionEvent */ NOT NULL;
ALTER TABLE Game MODIFY speedCost int NOT NULL DEFAULT 500;

CREATE INDEX ProductionEvent_globalId ON ProductionEvent(globalProductionEventId);
CREATE UNIQUE INDEX TriggerDefinition_className ON TriggerDefinition(className);
CREATE INDEX TriggerInstance_playerId ON TriggerInstance(playerId);
