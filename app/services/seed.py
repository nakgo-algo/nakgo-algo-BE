from sqlalchemy.orm import Session

from app.models import Fine, FishSpecies, Regulation, Zone


def seed_reference_data(db: Session) -> None:
    if db.query(FishSpecies).count() == 0:
        species_rows = [
            FishSpecies(name="우럭", min_length=23, banned_months=[1, 2, 12], category="바다", fine="10만원"),
            FishSpecies(name="광어", min_length=35, banned_months=[1, 2, 3, 4, 11, 12], category="바다", fine="10만원"),
            FishSpecies(name="감성돔", min_length=25, banned_months=[5, 6], category="바다", fine="10만원"),
            FishSpecies(name="참돔", min_length=24, banned_months=[5, 6], category="바다", fine="10만원"),
            FishSpecies(name="농어", min_length=30, banned_months=[5, 6, 7], category="바다", fine="10만원"),
            FishSpecies(name="볼락", min_length=15, banned_months=[4, 5], category="바다", fine="10만원"),
            FishSpecies(name="조피볼락", min_length=23, banned_months=[12, 1, 2], category="바다", fine="10만원"),
            FishSpecies(name="놀래미", min_length=20, banned_months=[11, 12], category="바다", fine="10만원"),
            FishSpecies(name="도다리", min_length=15, banned_months=[12, 1, 2], category="바다", fine="10만원"),
            FishSpecies(name="대구", min_length=35, banned_months=[1, 2, 3], category="바다", fine="10만원"),
            FishSpecies(name="방어", min_length=30, banned_months=[], category="바다", fine="10만원"),
            FishSpecies(name="갈치", min_length=18, banned_months=[7, 8], category="바다", fine="10만원"),
            FishSpecies(name="고등어", min_length=21, banned_months=[], category="바다", fine="5만원"),
            FishSpecies(name="삼치", min_length=30, banned_months=[], category="바다", fine="5만원"),
            FishSpecies(name="참조기", min_length=15, banned_months=[5, 6, 7], category="바다", fine="10만원"),
            FishSpecies(name="전갱이", min_length=15, banned_months=[], category="바다", fine="5만원"),
            FishSpecies(name="문어", min_length=0, banned_months=[5, 6], category="바다", fine="10만원"),
            FishSpecies(name="쭈꾸미", min_length=0, banned_months=[5, 6, 7, 8], category="바다", fine="10만원"),
            FishSpecies(name="배스", min_length=0, banned_months=[], category="민물", fine="없음"),
            FishSpecies(name="붕어", min_length=0, banned_months=[5, 6], category="민물", fine="5만원"),
            FishSpecies(name="쏘가리", min_length=18, banned_months=[5, 6], category="민물", fine="10만원"),
            FishSpecies(name="메기", min_length=0, banned_months=[5, 6], category="민물", fine="5만원"),
            FishSpecies(name="잉어", min_length=0, banned_months=[5, 6], category="민물", fine="5만원"),
        ]
        db.add_all(species_rows)
        db.flush()

        # species_rows index: 0=우럭 1=광어 2=감성돔 3=참돔 4=농어 5=볼락 6=조피볼락
        # 7=놀래미 8=도다리 9=대구 10=방어 11=갈치 12=고등어 13=삼치 14=참조기
        # 15=전갱이 16=문어 17=쭈꾸미 18=배스 19=붕어 20=쏘가리 21=메기 22=잉어

        regulation_rows = [
            # 경기도
            Regulation(region_id="gyeonggi", region="경기도", species_id=species_rows[0].id, min_length=23, banned_period="12월~2월", fine="10만원"),
            Regulation(region_id="gyeonggi", region="경기도", species_id=species_rows[1].id, min_length=35, banned_period="11월~4월", fine="10만원"),
            Regulation(region_id="gyeonggi", region="경기도", species_id=species_rows[19].id, min_length=0, banned_period="5월~6월", fine="5만원"),
            Regulation(region_id="gyeonggi", region="경기도", species_id=species_rows[20].id, min_length=18, banned_period="5월~6월", fine="10만원"),
            # 서울
            Regulation(region_id="seoul", region="서울", species_id=species_rows[18].id, min_length=0, banned_period="없음", fine="없음"),
            Regulation(region_id="seoul", region="서울", species_id=species_rows[19].id, min_length=0, banned_period="5월~6월", fine="5만원"),
            Regulation(region_id="seoul", region="서울", species_id=species_rows[20].id, min_length=18, banned_period="5월~6월", fine="10만원"),
            Regulation(region_id="seoul", region="서울", species_id=species_rows[22].id, min_length=0, banned_period="5월~6월", fine="5만원"),
            # 인천
            Regulation(region_id="incheon", region="인천", species_id=species_rows[0].id, min_length=23, banned_period="12월~2월", fine="10만원"),
            Regulation(region_id="incheon", region="인천", species_id=species_rows[2].id, min_length=25, banned_period="5월~6월", fine="10만원"),
            Regulation(region_id="incheon", region="인천", species_id=species_rows[7].id, min_length=20, banned_period="11월~12월", fine="10만원"),
            Regulation(region_id="incheon", region="인천", species_id=species_rows[14].id, min_length=15, banned_period="5월~7월", fine="10만원"),
            # 강원
            Regulation(region_id="gangwon", region="강원도", species_id=species_rows[0].id, min_length=23, banned_period="12월~2월", fine="10만원"),
            Regulation(region_id="gangwon", region="강원도", species_id=species_rows[1].id, min_length=35, banned_period="11월~4월", fine="10만원"),
            Regulation(region_id="gangwon", region="강원도", species_id=species_rows[9].id, min_length=35, banned_period="1월~3월", fine="10만원"),
            Regulation(region_id="gangwon", region="강원도", species_id=species_rows[4].id, min_length=30, banned_period="5월~7월", fine="10만원"),
            Regulation(region_id="gangwon", region="강원도", species_id=species_rows[20].id, min_length=18, banned_period="5월~6월", fine="10만원"),
            # 충북
            Regulation(region_id="chungbuk", region="충청북도", species_id=species_rows[18].id, min_length=0, banned_period="없음", fine="없음"),
            Regulation(region_id="chungbuk", region="충청북도", species_id=species_rows[19].id, min_length=0, banned_period="5월~6월", fine="5만원"),
            Regulation(region_id="chungbuk", region="충청북도", species_id=species_rows[20].id, min_length=18, banned_period="5월~6월", fine="10만원"),
            Regulation(region_id="chungbuk", region="충청북도", species_id=species_rows[21].id, min_length=0, banned_period="5월~6월", fine="5만원"),
            # 충남
            Regulation(region_id="chungnam", region="충청남도", species_id=species_rows[0].id, min_length=23, banned_period="12월~2월", fine="10만원"),
            Regulation(region_id="chungnam", region="충청남도", species_id=species_rows[2].id, min_length=25, banned_period="5월~6월", fine="10만원"),
            Regulation(region_id="chungnam", region="충청남도", species_id=species_rows[14].id, min_length=15, banned_period="5월~7월", fine="10만원"),
            Regulation(region_id="chungnam", region="충청남도", species_id=species_rows[17].id, min_length=0, banned_period="5월~8월", fine="10만원"),
            # 세종
            Regulation(region_id="sejong", region="세종", species_id=species_rows[18].id, min_length=0, banned_period="없음", fine="없음"),
            Regulation(region_id="sejong", region="세종", species_id=species_rows[19].id, min_length=0, banned_period="5월~6월", fine="5만원"),
            # 대전
            Regulation(region_id="daejeon", region="대전", species_id=species_rows[18].id, min_length=0, banned_period="없음", fine="없음"),
            Regulation(region_id="daejeon", region="대전", species_id=species_rows[19].id, min_length=0, banned_period="5월~6월", fine="5만원"),
            Regulation(region_id="daejeon", region="대전", species_id=species_rows[20].id, min_length=18, banned_period="5월~6월", fine="10만원"),
            # 전북
            Regulation(region_id="jeonbuk", region="전라북도", species_id=species_rows[0].id, min_length=23, banned_period="12월~2월", fine="10만원"),
            Regulation(region_id="jeonbuk", region="전라북도", species_id=species_rows[2].id, min_length=25, banned_period="5월~6월", fine="10만원"),
            Regulation(region_id="jeonbuk", region="전라북도", species_id=species_rows[11].id, min_length=18, banned_period="7월~8월", fine="10만원"),
            Regulation(region_id="jeonbuk", region="전라북도", species_id=species_rows[14].id, min_length=15, banned_period="5월~7월", fine="10만원"),
            # 전남
            Regulation(region_id="jeonnam", region="전라남도", species_id=species_rows[0].id, min_length=23, banned_period="12월~2월", fine="10만원"),
            Regulation(region_id="jeonnam", region="전라남도", species_id=species_rows[2].id, min_length=25, banned_period="5월~6월", fine="10만원"),
            Regulation(region_id="jeonnam", region="전라남도", species_id=species_rows[3].id, min_length=24, banned_period="5월~6월", fine="10만원"),
            Regulation(region_id="jeonnam", region="전라남도", species_id=species_rows[4].id, min_length=30, banned_period="5월~7월", fine="10만원"),
            Regulation(region_id="jeonnam", region="전라남도", species_id=species_rows[16].id, min_length=0, banned_period="5월~6월", fine="10만원"),
            # 광주
            Regulation(region_id="gwangju", region="광주", species_id=species_rows[18].id, min_length=0, banned_period="없음", fine="없음"),
            Regulation(region_id="gwangju", region="광주", species_id=species_rows[19].id, min_length=0, banned_period="5월~6월", fine="5만원"),
            # 경북
            Regulation(region_id="gyeongbuk", region="경상북도", species_id=species_rows[0].id, min_length=23, banned_period="12월~2월", fine="10만원"),
            Regulation(region_id="gyeongbuk", region="경상북도", species_id=species_rows[1].id, min_length=35, banned_period="11월~4월", fine="10만원"),
            Regulation(region_id="gyeongbuk", region="경상북도", species_id=species_rows[9].id, min_length=35, banned_period="1월~3월", fine="10만원"),
            Regulation(region_id="gyeongbuk", region="경상북도", species_id=species_rows[2].id, min_length=25, banned_period="5월~6월", fine="10만원"),
            # 경남
            Regulation(region_id="gyeongnam", region="경상남도", species_id=species_rows[0].id, min_length=23, banned_period="12월~2월", fine="10만원"),
            Regulation(region_id="gyeongnam", region="경상남도", species_id=species_rows[2].id, min_length=25, banned_period="5월~6월", fine="10만원"),
            Regulation(region_id="gyeongnam", region="경상남도", species_id=species_rows[3].id, min_length=24, banned_period="5월~6월", fine="10만원"),
            Regulation(region_id="gyeongnam", region="경상남도", species_id=species_rows[10].id, min_length=30, banned_period="없음", fine="10만원"),
            Regulation(region_id="gyeongnam", region="경상남도", species_id=species_rows[16].id, min_length=0, banned_period="5월~6월", fine="10만원"),
            # 대구
            Regulation(region_id="daegu", region="대구", species_id=species_rows[18].id, min_length=0, banned_period="없음", fine="없음"),
            Regulation(region_id="daegu", region="대구", species_id=species_rows[19].id, min_length=0, banned_period="5월~6월", fine="5만원"),
            Regulation(region_id="daegu", region="대구", species_id=species_rows[20].id, min_length=18, banned_period="5월~6월", fine="10만원"),
            # 부산
            Regulation(region_id="busan", region="부산", species_id=species_rows[0].id, min_length=23, banned_period="12월~2월", fine="10만원"),
            Regulation(region_id="busan", region="부산", species_id=species_rows[2].id, min_length=25, banned_period="5월~6월", fine="10만원"),
            Regulation(region_id="busan", region="부산", species_id=species_rows[3].id, min_length=24, banned_period="5월~6월", fine="10만원"),
            Regulation(region_id="busan", region="부산", species_id=species_rows[10].id, min_length=30, banned_period="없음", fine="10만원"),
            Regulation(region_id="busan", region="부산", species_id=species_rows[11].id, min_length=18, banned_period="7월~8월", fine="10만원"),
            # 울산
            Regulation(region_id="ulsan", region="울산", species_id=species_rows[0].id, min_length=23, banned_period="12월~2월", fine="10만원"),
            Regulation(region_id="ulsan", region="울산", species_id=species_rows[2].id, min_length=25, banned_period="5월~6월", fine="10만원"),
            Regulation(region_id="ulsan", region="울산", species_id=species_rows[9].id, min_length=35, banned_period="1월~3월", fine="10만원"),
            # 제주
            Regulation(region_id="jeju", region="제주도", species_id=species_rows[0].id, min_length=23, banned_period="12월~2월", fine="10만원"),
            Regulation(region_id="jeju", region="제주도", species_id=species_rows[2].id, min_length=25, banned_period="5월~6월", fine="10만원"),
            Regulation(region_id="jeju", region="제주도", species_id=species_rows[3].id, min_length=24, banned_period="5월~6월", fine="10만원"),
            Regulation(region_id="jeju", region="제주도", species_id=species_rows[4].id, min_length=30, banned_period="5월~7월", fine="10만원"),
            Regulation(region_id="jeju", region="제주도", species_id=species_rows[5].id, min_length=15, banned_period="4월~5월", fine="10만원"),
            Regulation(region_id="jeju", region="제주도", species_id=species_rows[16].id, min_length=0, banned_period="5월~6월", fine="10만원"),
            # 서해
            Regulation(region_id="westSea", region="서해", species_id=species_rows[0].id, min_length=23, banned_period="12월~2월", fine="10만원"),
            Regulation(region_id="westSea", region="서해", species_id=species_rows[2].id, min_length=25, banned_period="5월~6월", fine="10만원"),
            Regulation(region_id="westSea", region="서해", species_id=species_rows[7].id, min_length=20, banned_period="11월~12월", fine="10만원"),
            Regulation(region_id="westSea", region="서해", species_id=species_rows[14].id, min_length=15, banned_period="5월~7월", fine="10만원"),
            Regulation(region_id="westSea", region="서해", species_id=species_rows[17].id, min_length=0, banned_period="5월~8월", fine="10만원"),
            # 동해
            Regulation(region_id="eastSea", region="동해", species_id=species_rows[0].id, min_length=23, banned_period="12월~2월", fine="10만원"),
            Regulation(region_id="eastSea", region="동해", species_id=species_rows[1].id, min_length=35, banned_period="11월~4월", fine="10만원"),
            Regulation(region_id="eastSea", region="동해", species_id=species_rows[9].id, min_length=35, banned_period="1월~3월", fine="10만원"),
            Regulation(region_id="eastSea", region="동해", species_id=species_rows[4].id, min_length=30, banned_period="5월~7월", fine="10만원"),
            Regulation(region_id="eastSea", region="동해", species_id=species_rows[12].id, min_length=21, banned_period="없음", fine="5만원"),
            # 남해
            Regulation(region_id="southSea", region="남해", species_id=species_rows[0].id, min_length=23, banned_period="12월~2월", fine="10만원"),
            Regulation(region_id="southSea", region="남해", species_id=species_rows[2].id, min_length=25, banned_period="5월~6월", fine="10만원"),
            Regulation(region_id="southSea", region="남해", species_id=species_rows[3].id, min_length=24, banned_period="5월~6월", fine="10만원"),
            Regulation(region_id="southSea", region="남해", species_id=species_rows[4].id, min_length=30, banned_period="5월~7월", fine="10만원"),
            Regulation(region_id="southSea", region="남해", species_id=species_rows[10].id, min_length=30, banned_period="없음", fine="10만원"),
            Regulation(region_id="southSea", region="남해", species_id=species_rows[16].id, min_length=0, banned_period="5월~6월", fine="10만원"),
        ]
        db.add_all(regulation_rows)

    if db.query(Fine).count() == 0:
        fine_rows = [
            Fine(species="우럭", violation="체장 미달 (23cm 미만 포획)", fine_amount="10만원", legal_basis="수산업법 제64조"),
            Fine(species="광어", violation="체장 미달 (35cm 미만 포획)", fine_amount="10만원", legal_basis="수산업법 제64조"),
            Fine(species="감성돔", violation="체장 미달 (25cm 미만 포획)", fine_amount="10만원", legal_basis="수산업법 제64조"),
            Fine(species="참돔", violation="체장 미달 (24cm 미만 포획)", fine_amount="10만원", legal_basis="수산업법 제64조"),
            Fine(species="농어", violation="체장 미달 (30cm 미만 포획)", fine_amount="10만원", legal_basis="수산업법 제64조"),
            Fine(species="고등어", violation="체장 미달 (21cm 미만 포획)", fine_amount="5만원", legal_basis="수산업법 제64조"),
            Fine(species="쏘가리", violation="체장 미달 (18cm 미만 포획)", fine_amount="10만원", legal_basis="내수면어업법 제28조"),
            Fine(species="일반", violation="금어기 중 포획", fine_amount="30만원 이하", legal_basis="수산업법 제97조"),
            Fine(species="일반", violation="금지구역 내 낚시", fine_amount="100만원 이하", legal_basis="수산업법 제97조"),
            Fine(species="일반", violation="유어 낚시 무신고", fine_amount="50만원 이하", legal_basis="수산업법 제55조"),
            Fine(species="일반", violation="낚시 제한수량 초과", fine_amount="30만원 이하", legal_basis="낚시관리및육성법 제25조"),
            Fine(species="일반", violation="낚시터 쓰레기 투기", fine_amount="100만원 이하", legal_basis="낚시관리및육성법 제25조"),
            Fine(species="일반", violation="금지된 낚시도구 사용", fine_amount="50만원 이하", legal_basis="낚시관리및육성법 제25조"),
            Fine(species="일반", violation="야간 낚시 금지구역 위반", fine_amount="30만원 이하", legal_basis="낚시관리및육성법 제25조"),
        ]
        db.add_all(fine_rows)

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
