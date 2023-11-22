CREATE TABLE respgeo_FR(
   Zone_geographique    VARCHAR(6) NOT NULL PRIMARY KEY
  ,Responsable_regional VARCHAR(9) NOT NULL
);
INSERT INTO respgeo_FR(Zone_geographique,Responsable_regional) VALUES ('Nord','Gabrielle');
INSERT INTO respgeo_FR(Zone_geographique,Responsable_regional) VALUES ('Sud','Alaine');
INSERT INTO respgeo_FR(Zone_geographique,Responsable_regional) VALUES ('Centre','Olivia');
INSERT INTO respgeo_FR(Zone_geographique,Responsable_regional) VALUES ('Nord','Admin');
INSERT INTO respgeo_FR(Zone_geographique,Responsable_regional) VALUES ('Sud','Admin');
INSERT INTO respgeo_FR(Zone_geographique,Responsable_regional) VALUES ('Centre','Admin');
