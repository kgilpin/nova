
from nova.api import query
from nova.engine import store
from nova.ProductionEvent import ProductionEvent
from nova.GlobalProductionEvent import GlobalProductionEvent

pes = store.get().fetchObjectsOfClass(ProductionEvent, clauses="WHERE globalProductionEventId = 0")
count = 0
for pe in pes:
	gpes = store.get().fetchObjectsOfClass(GlobalProductionEvent, clauses="WHERE gameId = %d AND executionTime <= '%s' ORDER BY executionTime DESC LIMIT 1" % \
		( pe.game().sqlObjRef(), query.formatMySQLDate(pe.executionTime()) ))
	if len(gpes):
		pe.setGlobalProductionEvent(gpes[0])
		count += 1
	else:
		print 'No GlobalProductionEvent found for %d' % pe.serialNum()

print 'Updated %d ProductionEvents' % count
store.get().saveChanges()
