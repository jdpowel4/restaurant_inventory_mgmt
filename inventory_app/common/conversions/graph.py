from collections import defaultdict, deque
from decimal import Decimal

from inventory_app.common.conversions.dto import ConversionEdge, ConversionPath
from inventory_app.common.conversions.exceptions import MissingConversionError



class ConversionGraph:

    def __init__(self):

        self._graph = defaultdict(list)

    def _add_edge(
            self,
            from_unit,
            to_unit,
            multiplier,
            source
    ):
        
        edge = ConversionEdge(
            from_unit,
            to_unit,
            multiplier,
            source
        )

        self._graph[from_unit].append(edge)

    def neighbors(self, unit):
        return self._graph.get(unit, [])
    

    def add_bidirectional_edge(
        self,
        from_unit,
        to_unit,
        multiplier,
        source
    ):
        self._add_edge(
            from_unit,
            to_unit,
            multiplier,
            source
        )

        self._add_edge(
            to_unit,
            from_unit,
            Decimal("1") / multiplier,
            source
        )

    
    def find_path(
        self,
        from_unit,
        to_unit
    ):
        start = from_unit.id
        end = to_unit.id
        if start == end:
            return ConversionPath([], Decimal("1"))

        queue = deque()

        queue.append(
            (
                start,
                [],
                Decimal("1")
            )
        )

        visited = {start}

        while queue:

            node, edges, multiplier = queue.popleft()

            for edge in self.neighbors(node):

                if edge.to_unit_id in visited:
                    continue

                new_multiplier = multiplier * edge.multiplier

                new_path = edges + [edge]

                if edge.to_unit_id == end:
                    return ConversionPath(
                        new_path,
                        new_multiplier
                    )
                
                visited.add(edge.to_unit_id)

                queue.append(
                    (
                        edge.to_unit_id,
                        new_path,
                        new_multiplier
                    )
                )
        
        raise MissingConversionError(
            f"No conversion path from {from_unit} to {to_unit}"
        )