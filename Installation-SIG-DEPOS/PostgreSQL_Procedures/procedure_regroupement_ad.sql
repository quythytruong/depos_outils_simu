CREATE OR REPLACE PROCEDURE public.regroupement_ad(
	volume_max numeric,
	percent_volume numeric)
LANGUAGE 'plpgsql'

AS $BODY$
declare
	big_ad RECORD;
	small_ad_intersect RECORD;
	info_ajout_ad text;
	vol_cumul double precision;
	distance geometry;
	id_ad integer;
begin
	ALTER TABLE ad_potentielles ADD COLUMN vol_dechet_ini double precision;
	UPDATE ad_potentielles SET vol_dechet_ini = vol_dechet_m3 * percent_volume;
	DROP TABLE IF EXISTS ad_optim; 
	CREATE TABLE ad_optim(
		id integer, -- colonne id de la table intersections ou proj_bati_route
		the_geom geometry,
		vol_dechet_m3 double precision,
		id_optim integer primary key, -- id unique
		buffer geometry,
		vol_dechet_ini double precision
	);
	DROP TABLE IF EXISTS dist_gisement_ad_optim;
	CREATE TABLE dist_gisement_ad_optim(
		id_gisement integer,
		id_ad integer,
		geom_gisement geometry
	);
	
	SELECT * INTO big_ad 
	FROM ad_potentielles
	WHERE vol_dechet_ini <= volume_max	
	ORDER BY vol_dechet_m3 DESC LIMIT 1;
		
	WHILE NOT big_ad IS NULL LOOP
		info_ajout_ad := big_ad.id_optim || ' - ' || big_ad.vol_dechet_ini || 'm3';
		id_ad := big_ad.id_optim ;
		RAISE NOTICE '1/ AD %', info_ajout_ad;
	
		-- Ajout dans la table final
		INSERT INTO ad_optim (id, id_optim, vol_dechet_m3,vol_dechet_ini, the_geom, buffer) VALUES 
			(big_ad.id,	big_ad.id_optim,
			 big_ad.vol_dechet_m3, big_ad.vol_dechet_ini,
			 big_ad.the_geom, big_ad.buffer);

		-- On se place dans ad_regroupees_final pour avoir les nouveaux volumes de déchets
		SELECT * INTO big_ad FROM ad_optim tbl WHERE tbl.id_optim = big_ad.id_optim;
		
		-- Supprime de la première table
		DELETE FROM ad_potentielles WHERE id_optim = id_ad;
		RAISE NOTICE '2) Supprime de la table ad_potentielle AD n°%', id_ad || ' de volume ' ||big_ad.vol_dechet_ini;
		vol_cumul:= big_ad.vol_dechet_ini;
		
		-- Recherche la plus petite AD qui l'intersecte et dont les déchets pourraient être  
		-- déplacées sans que le tas de déchets sur la grande AD dépasse 500m3
		SELECT 
			tbl1.*, 
			tbl1.vol_dechet_ini + vol_cumul as somme_dechets 
		INTO small_ad_intersect
		FROM ad_potentielles tbl1
		WHERE 
			tbl1.id_optim <> id_ad AND
			ST_INTERSECTS(tbl1.buffer, big_ad.buffer) AND
			tbl1.vol_dechet_ini + vol_cumul <= volume_max
			ORDER BY tbl1.vol_dechet_ini ASC LIMIT 1;
		
		WHILE NOT small_ad_intersect IS NULL LOOP
			RAISE NOTICE '3) AD %', small_ad_intersect.id_optim || ' - ' || 
						small_ad_intersect.vol_dechet_ini || 'm3';
			vol_cumul := vol_cumul + small_ad_intersect.vol_dechet_ini ;
			UPDATE ad_optim
			SET
				vol_dechet_m3 = vol_dechet_m3 + small_ad_intersect.vol_dechet_m3,
				vol_dechet_ini = vol_dechet_ini + small_ad_intersect.vol_dechet_ini
			WHERE id_optim = id_ad;
			
			info_ajout_ad := '4/ Ajoute AD id_optim. ' || small_ad_intersect.id_optim 
							|| ', de volume ' || small_ad_intersect.vol_dechet_ini ||' m3 '
							|| ' dans AD id_optim.' || id_ad
							|| ' de volume final ' || small_ad_intersect.somme_dechets ||' m3 ';
			RAISE NOTICE '%', info_ajout_ad;
			
			-- Renseigne la distance entre le gisement et l'AD finale
			-- TO DO LATER
			
			-- Supprime de la première table
			DELETE FROM ad_potentielles WHERE id_optim = small_ad_intersect.id_optim;
			
			-- Recherche à nouveau les petites AD potentielles qui peuvent être fusionnées
			SELECT 
				tbl1.*, 
				tbl1.vol_dechet_ini + big_ad.vol_dechet_ini as somme_dechets 
			INTO small_ad_intersect
			FROM 
				ad_potentielles tbl1
			WHERE 
				tbl1.id_optim <> id_ad AND
				ST_INTERSECTS(tbl1.buffer, big_ad.buffer) AND
				tbl1.vol_dechet_ini + vol_cumul <= volume_max
			ORDER BY tbl1.vol_dechet_m3 ASC	LIMIT 1;
			END LOOP;
		
		-- La plus grande AD de moins de 500m3
		SELECT * INTO big_ad 
		FROM ad_potentielles
		WHERE vol_dechet_ini <= volume_max
		ORDER BY vol_dechet_m3 DESC	LIMIT 1;
		
		END LOOP;
	-- Insère les AD qui restent (> 500 m3)
	INSERT INTO ad_optim (id, id_optim, the_geom, buffer, vol_dechet_m3,vol_dechet_ini)
	SELECT id, id_optim, the_geom, buffer, vol_dechet_m3, vol_dechet_ini
	FROM ad_potentielles;
end; $BODY$;