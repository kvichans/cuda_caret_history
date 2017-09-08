# -*- coding: utf-8 -*-
''' Plugin for CudaText editor
    Отслеживание истории перемещения курсора (каретки).
    Последующее восстановление позиции каретки
Authors:
    github.com/eastorwest
    Andrey Kvichansky    (kvichans on github.com)
Version:
    '1.0.02 2017-08-15'
ToDo: (see end of file)
'''

import  os, sys, json
from collections import namedtuple, OrderedDict as odict

import  cudatext            as app
from    cudatext        import ed
import  cudax_lib           as apx

pass;                           LOG = (-1==-1)  # Do or dont logging.
from    cudax_lib       import  log

HistItem    = namedtuple('HistItem', ['x', 'y', 'x_', 'y_'])    # x/y - caret, x_/y_ - end of selection (-1/-1 if no sel)
GAP_SIZE    = apx.get_opt('curshist_gap_size', 10)              # Минимальное отличие по строкам (y) от предыдущего значения для сохранения
HIST_MAX    = apx.get_opt('curshist_max_history', 5)            # Максимальный размер истории для каждого таба
#SAVE_HIST   = apx.get_opt('curshist_save_history', False)
#CFG_JSON    = app.app_path(app.APP_DIR_SETTINGS)+os.sep+'cuda_curshist.json'

class Command:
    history = {}        # {tab_id:([HistItem])}
    poses   = {}        # {tab_id:pos}
    
    skip_rec= False     # Antiloop

    def __init__(self):
        pass
#       if SAVE_HIST:
#           stores  = json.loads(open(CFG_JSON).read(), object_pairs_hook=odict) \
#                       if os.path.exists(CFG_JSON) and os.path.getsize(CFG_JSON) != 0 else \
#                     odict()
#           self.history = stores.get('history', history)

    def on_close(self, ed_self):
        tab_id  = ed_self.get_prop(app.PROP_TAB_ID) # уникальный ID вкладки
        if tab_id in self.history:
            del self.history[tab_id]
            del self.poses[  tab_id]
    
    def on_caret(self, ed_self):
        if self.skip_rec:
            self.skip_rec = False
            return 
            
        crts    = ed.get_carets()
        if len(crts)>1:
            pass;              #LOG and log('skip: many carets',())
            return 
        new_item= HistItem(*crts[0])
        pass;                  #LOG and log('new_item={}',(new_item))
        tab_id  = ed_self.get_prop(app.PROP_TAB_ID) # уникальный ID вкладки
        if tab_id not in self.history:
            self.history[tab_id]    = [new_item]
            self.poses[  tab_id]    = 0
            pass;              #LOG and log('new tab',())
            return 
        hist,   \
        pos     = self.history[tab_id] \
                , self.poses[  tab_id]
        
        pre_item= hist[pos]
        if abs(pre_item.y - new_item.y) > GAP_SIZE:
            # Дальний скачок
            # - Начать новое наращивание истории
            # - Запомнить текущую каретку (или выделение) для последующего перехода
            del hist[pos+1:]
            hist    += [new_item]
            self.poses[tab_id] = pos+1
            if len(hist)>HIST_MAX:
                del hist[0]
                self.poses[tab_id] -= 1
            pass;              #LOG and log('long gap pos,hist={}',(self.poses[tab_id], hist))
        else:
            # Ближний скачок
            # - Изменяем данные о текущем положении в истории
            # - Сохраняем возможность для forward-перехода
            pass;              #LOG and log('short gap',())
            hist[pos]   = new_item
       #def on_caret
  
    def move_backward(self):
        tab_id  = ed.get_prop(app.PROP_TAB_ID) # уникальный ID вкладки
        if  tab_id not in self.poses or \
            self.poses[tab_id]==0:
            pass;              #LOG and log('skip: no tab or no more to back',())
            return 
        self.poses[tab_id] -= 1
        self._move_caret(self.history[tab_id][self.poses[tab_id]])
  
    def move_forward(self):
        tab_id  = ed.get_prop(app.PROP_TAB_ID) # уникальный ID вкладки
        if  tab_id not in self.poses or \
            self.poses[tab_id]>=(len(self.history[tab_id])-1):
            pass;              #LOG and log('skip: no tab or no more to forw',())
            return 
        self.poses[tab_id] += 1
        self._move_caret(self.history[tab_id][self.poses[tab_id]])

    def _move_caret(self, item):
        self.skip_rec = True
        ed.set_caret(item.x, item.y, item.x_, item.y_)
  
