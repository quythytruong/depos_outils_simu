CREATE OR REPLACE PROCEDURE public.buffer_ad(
	vol1 numeric,
	vol2 numeric,
	vol3 numeric,
	radius1 numeric,
	radius2 numeric,
	radius3 numeric,
	radius4 numeric,
	percent_volume numeric)
LANGUAGE 'plpgsql'

AS $BODY$
declare
-- variable declaration
begin
-- stored procedure body
	ALTER TABLE ad_potentielles DROP COLUMN IF EXISTS buffer;
	ALTER TABLE ad_potentielles ADD COLUMN buffer geometry;

	UPDATE ad_potentielles SET buffer = ST_BUFFER(the_geom, radius1) 
	WHERE vol_dechet_m3*percent_volume <= vol1;

	UPDATE ad_potentielles SET buffer = ST_BUFFER(the_geom, radius2) 
	WHERE vol_dechet_m3*percent_volume > vol1 AND vol_dechet_m3*percent_volume<= vol2;

	UPDATE ad_potentielles SET buffer = ST_BUFFER(the_geom, radius3) 
	WHERE vol_dechet_m3*percent_volume > vol2 AND vol_dechet_m3*percent_volume <= vol3;

	UPDATE ad_potentielles SET buffer = ST_BUFFER(the_geom, radius4) 
	WHERE vol_dechet_m3*percent_volume > vol3;

end; $BODY$;