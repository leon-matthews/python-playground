
-- Schema
-- ======
CREATE TABLE ecomdb (
    site TEXT,
    name TEXT,
    data_dump TEXT,
    category TEXT,
    sub_cat TEXT,
    sub_sub_cat TEXT,
    is_valid TEXT,
    id INTEGER PRIMARY KEY
);


-- count
sqlite> SELECT count(*) FROM ecomdb;
1090


-- class blue_item extends ecom_base_item
INSERT INTO "ecomdb" VALUES('blueribbon','SAT024SCA                          ',
    '<wddxPacket version=''1.0''>
    <header/>
    <data>
    <struct>
    <var name=''php_class_name''><string>blue_item</string></var>
    <var name=''carton_size''><string></string></var>
    <var name=''name''><string>SAT024SCA                          </string></var>
    <var name=''category''><string>items</string></var>
    <var name=''sub_cat''><null/></var>
    <var name=''sub_sub_cat''><null/></var>
    <var name=''is_valid''><null/></var>
    <var name=''id''><null/></var>
    <var name=''full_name''><string>Serving Spoon</string></var>
    <var name=''thumbnail''><string>/uploaded/item/tn_1245902981.jpg</string></var>
    <var name=''photo''><string>/uploaded/item/1245902981.jpg</string></var>
    <var name=''short_desc''><null/></var>
    <var name=''long_desc''><null/></var>
    <var name=''price''><string>15.75</string></var>
    </struct>
    </data>
    </wddxPacket>',
'items','','','t',1777);


-- class blue_listing extends ecom_base_item
INSERT INTO "ecomdb" VALUES('blueribbon','counter',
    '<wddxPacket version=''1.0''>
    <header/>
    <data>
    <struct>
    <var name=''php_class_name''><string>blue_listing</string></var>
    <var name=''links''><struct><var name=''74115''><string>CAKE STAND-S/S, 300mm, FLAT BASE</string></var>
    <var name=''74120''><string>CAKE STAND-S/S, 300mm, SHORT BASE</string></var>
    <var name=''74125''><string>CAKE STAND-S/S, 300mm LONG BASE</string></var>
    <var name=''74140''><string>CAKE COVER-CLEAR,W/CHR. HDL.</string></var>
    <var name=''74141''><string>CAKE COVER-CLEAR,W/MLD. HDL.</string></var>
    <var name=''74144''><string>CAKE COVER-ACRYLIC,DOME STYLE,300mm </string></var>
    <var name=''74145''><string>CAKE COVER-ACRYLIC,230mm HIGH</string></var>
    <var name=''74150''><string>PIE &amp; CAKE RACK-3 TIER, CHROME</string></var>
    </struct>
    </var>
    <var name=''name''><string>counter</string></var>
    <var name=''category''><string>barware</string></var>
    <var name=''sub_cat''><null/></var>
    <var name=''sub_sub_cat''><null/></var>
    <var name=''is_valid''><string>t</string></var>
    <var name=''id''><string>1491</string></var>
    <var name=''full_name''><string>Cake Stands and Covers</string></var>
    <var name=''thumbnail''><null/></var>
    <var name=''photo''><string>/uploaded/listing/1123989752.jpg</string></var>
    <var name=''short_desc''><null/></var>
    <var name=''long_desc''><null/></var>
    <var name=''price''><null/></var>
    </struct>
    </data>
    </wddxPacket>',
'barware','','','t',1491);
