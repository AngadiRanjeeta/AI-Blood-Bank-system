from sqlalchemy import text

FIND_CANDIDATES_SQL = text("""
    SELECT 
        h.id,
        h.hname,
        h.hcity,
        (
            6371 * ACOS(
                COS(RADIANS(:lat)) *
                COS(RADIANS(h.latitude)) *
                COS(RADIANS(h.longitude) - RADIANS(:lon)) +
                SIN(RADIANS(:lat)) *
                SIN(RADIANS(h.latitude))
            )
        ) AS distance_km,
        COUNT(b.bid) AS stock_units
    FROM hospitals h
    JOIN bloodinfo b ON h.id = b.hid
    WHERE b.bg = :bg
    GROUP BY h.id
    ORDER BY distance_km ASC
    LIMIT 5;
""")