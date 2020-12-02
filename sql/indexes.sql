-- Ensure that playerName and User.name are unique to their contexts
CREATE UNIQUE INDEX User_uniqueName ON User (name);
CREATE UNIQUE INDEX Player_uniqueName ON Player (gameId, name);

-- Indexes for common queries, see nova.api.query
CREATE INDEX Star_gameId ON Star (gameId);
CREATE INDEX Star_ownerId ON Star (ownerId);
CREATE INDEX ArrivalEvent_playerId ON ArrivalEvent (playerId);
CREATE INDEX SpyProbeEvent_playerId ON SpyProbeEvent (playerId);
CREATE INDEX DeathProbeEvent_playerId ON DeathProbeEvent (playerId);
CREATE INDEX FieryDeathEvent_playerId ON FieryDeathEvent (playerId);
CREATE INDEX BattleEvent_playerId ON BattleEvent (playerId);
CREATE INDEX DepartureEvent_playerId ON DepartureEvent (playerId);
CREATE INDEX ProductionEvent_globalId ON ProductionEvent(globalProductionEventId);
