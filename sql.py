import sqlite3

class SQLighter:

    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def get_subscriptions(self, status = True):
        """Получаем всех активных подписчиков бота"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM `subscriptions` WHERE `status` = ?", (status,)).fetchall()

    def subscriber_exists(self, user_id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `subscriptions` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))    
    def add_subscriber(self, user_id, status ,video_done,signets,time,mems_done,sms_done,geo_done,x_short_done,x_long_done,accidents_done,wp_done,army_done,science_done,auto_done,x_comixes_done):
        """Добавляем нового подписчика"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `subscriptions` (`user_id`, `status`,`video_done`,`signets`,`registred_by`,`mems_done`,`sms_done`,`geo_done`,`x_short_done`,`x_long_done`,`x_comixes_done`,`accidents_done`,`world_public_done`,`army_done`,`science_done`,`auto_done`) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (user_id, status ,video_done,signets,time,mems_done,sms_done,geo_done,x_short_done,x_long_done,accidents_done,wp_done,army_done,science_done,auto_done,x_comixes_done))

    def video_watched(self,user_id):
        with self.connection:
            a = self.cursor.execute(f"SELECT video_done FROM `subscriptions` WHERE `user_id` = {user_id}").fetchone()
            return a[0]
        
    def update_watched(self,user_id,video_done):
        with self.connection:
             return self.cursor.execute("UPDATE `subscriptions` SET `video_done` = ? WHERE `user_id` = ?", (video_done, user_id))
            
    def mems_watched(self,user_id):
        with self.connection:
            a = self.cursor.execute(f"SELECT mems_done FROM `subscriptions` WHERE `user_id` = {user_id}").fetchone()
            return a[0]

    def update_mems(self,user_id,mems_done):
        with self.connection:
             return self.cursor.execute("UPDATE `subscriptions` SET `mems_done` = ? WHERE `user_id` = ?", (mems_done, user_id))

    def sms_watched(self,user_id):
        with self.connection:
            a = self.cursor.execute(f"SELECT sms_done FROM `subscriptions` WHERE `user_id` = {user_id}").fetchone()
            return a[0]

    def update_sms(self,user_id,sms_done):
        with self.connection:
             return self.cursor.execute("UPDATE `subscriptions` SET `sms_done` = ? WHERE `user_id` = ?", (sms_done, user_id))


    def person_gallery(self,name):
        with self.connection:
            a = self.cursor.execute("SELECT * FROM person_media WHERE name=?",(name,)).fetchall()
            return [i for i in a[0][3:]]

    def geo_watched(self,user_id):
        with self.connection:
            a = self.cursor.execute(f"SELECT geo_done FROM `subscriptions` WHERE `user_id` = {user_id}").fetchone()
            return a[0]

    def update_geo(self,user_id,geo_done):
        with self.connection:
             return self.cursor.execute("UPDATE `subscriptions` SET `geo_done` = ? WHERE `user_id` = ?", (geo_done, user_id))

    
    def x_short_watched(self,user_id):
        with self.connection:
            a = self.cursor.execute(f"SELECT x_short_done FROM `subscriptions` WHERE `user_id` = {user_id}").fetchone()
            return a[0]

    def update_x_short(self,user_id,x_short_done):
        with self.connection:
             return self.cursor.execute("UPDATE `subscriptions` SET `x_short_done` = ? WHERE `user_id` = ?", (x_short_done, user_id))


    def x_long_watched(self,user_id):
        with self.connection:
            a = self.cursor.execute(f"SELECT x_long_done FROM `subscriptions` WHERE `user_id` = {user_id}").fetchone()
            return a[0]

    def update_x_long(self,user_id,x_long_done):
        with self.connection:
             return self.cursor.execute("UPDATE `subscriptions` SET `x_long_done` = ? WHERE `user_id` = ?", (x_long_done, user_id))

    def x_comixes_watched(self,user_id):
        with self.connection:
            a = self.cursor.execute(f"SELECT x_comixes_done FROM `subscriptions` WHERE `user_id` = {user_id}").fetchone()
            return a[0]

    def update_x_comixes(self,user_id,x_comixes_done):
        with self.connection:
             return self.cursor.execute("UPDATE `subscriptions` SET `x_comixes_done` = ? WHERE `user_id` = ?", (x_comixes_done, user_id))

    def get_signets(self,user_id):
        with self.connection:
            a = self.cursor.execute(f"SELECT signets FROM `subscriptions` WHERE `user_id` = {user_id}").fetchone()
            return a[0]
    def update_signents(self,user_id,new_signets):
        with self.connection:
             return self.cursor.execute("UPDATE `subscriptions` SET `signets` = ? WHERE `user_id` = ?", (new_signets, user_id))

    def get_accidents(self,user_id):
        with self.connection:
            a = self.cursor.execute(f"SELECT accidents_done FROM `subscriptions` WHERE `user_id` = {user_id}").fetchone()
            return a[0]        
    def update_accidents(self,user_id,new_accidents):
        with self.connection:
             return self.cursor.execute("UPDATE `subscriptions` SET `accidents_done` = ? WHERE `user_id` = ?", (new_accidents, user_id))

    def get_world_public(self,user_id):
        with self.connection:
            a = self.cursor.execute(f"SELECT world_public_done FROM `subscriptions` WHERE `user_id` = {user_id}").fetchone()
            return a[0]
    def update_world_public(self,user_id,new_wp):
        with self.connection:
             return self.cursor.execute("UPDATE `subscriptions` SET `world_public_done` = ? WHERE `user_id` = ?", (new_wp, user_id)) 
    def get_army(self,user_id):
        with self.connection:
            a = self.cursor.execute(f"SELECT army_done FROM `subscriptions` WHERE `user_id` = {user_id}").fetchone()
            return a[0]
    def update_army(self,user_id,new_army):
        with self.connection:
             return self.cursor.execute("UPDATE `subscriptions` SET `army_done` = ? WHERE `user_id` = ?", (new_army, user_id))

    def get_science(self,user_id):
        with self.connection:
            a = self.cursor.execute(f"SELECT science_done FROM `subscriptions` WHERE `user_id` = {user_id}").fetchone()
            return a[0]
    def update_science(self,user_id,new_sci):
        with self.connection:
             return self.cursor.execute("UPDATE `subscriptions` SET `science_done` = ? WHERE `user_id` = ?", (new_sci, user_id))        

    def get_auto(self,user_id):
        with self.connection:
            a = self.cursor.execute(f"SELECT auto_done FROM `subscriptions` WHERE `user_id` = {user_id}").fetchone()
            return a[0]

    def update_auto(self,user_id,new_auto):
        with self.connection:
             return self.cursor.execute("UPDATE `subscriptions` SET `auto_done` = ? WHERE `user_id` = ?", (new_auto, user_id))
    
    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()

    
