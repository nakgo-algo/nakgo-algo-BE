from sqlalchemy.orm import Session

from app.models import Fine, FishSpecies, Regulation, Zone


def seed_reference_data(db: Session) -> None:
    if db.query(FishSpecies).count() == 0:
        species_rows = [
            FishSpecies(name="우럭", min_length=23, banned_months=[1, 2, 12], category="바다", fine="10만원"),
            FishSpecies(name="광어", min_length=35, banned_months=[1, 2, 3, 4, 11, 12], category="바다", fine="10만원"),
        ]
        db.add_all(species_rows)
        db.flush()

        regulation_rows = [
            Regulation(
                region_id="gyeonggi",
                region="경기도",
                species_id=species_rows[0].id,
                min_length=23,
                banned_period="12월~2월",
                fine="10만원",
            ),
            Regulation(
                region_id="gyeonggi",
                region="경기도",
                species_id=species_rows[1].id,
                min_length=35,
                banned_period="11월~4월",
                fine="10만원",
            ),
        ]
        db.add_all(regulation_rows)

    if db.query(Fine).count() == 0:
        db.add(
            Fine(
                species="우럭",
                violation="체장 미달",
                fine_amount="10만원",
                legal_basis="수산업법 제XX조",
            )
        )

    if db.query(Zone).count() == 0:
        db.add(
            Zone(
                name="인천항 금지구역",
                type="fishing_ban",
                coordinates=[[126.123, 37.456], [126.124, 37.457], [126.125, 37.456]],
                description="연중 낚시 금지",
                period="연중",
            )
        )

    db.commit()
