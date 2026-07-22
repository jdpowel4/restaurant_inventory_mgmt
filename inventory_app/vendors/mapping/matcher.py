from rapidfuzz import process, fuzz
import re
from sqlalchemy.orm import Session

from inventory_app.vendors.mapping.dto import MatchResult
from inventory_app.ingredients.services import ingredient_service


class MapperMatcher:


    @staticmethod
    def find(
            session: Session,
            description: str
    ) -> list[MatchResult]:

        matcher = MapperMatcher()

        cleaned = matcher._normalize(description)


        ingredients = ingredient_service.get_all(session)


        lookup = {
            matcher._normalize(i.item.name): i
            for i in ingredients
        }

        matches = process.extract(
            cleaned,
            lookup.keys(),
            scorer=fuzz.token_set_ratio,
            limit = 5
        )
        
        results: list[MatchResult] = []

        for name, score, _ in matches:
            
            ingredient = lookup[name]

            results.append(
                MatchResult(
                    name=name,
                    ingredient=ingredient,
                    score=round(score)
                )
            )

        return results


    def _normalize(
            self,
            text: str
    ) -> str:

        text = text.lower()
        text = text.replace(","," ")
        text = re.sub(r"[^a-z0-9\s]", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text
