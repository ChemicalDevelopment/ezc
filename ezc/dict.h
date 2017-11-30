
#ifndef __DICT_H__
#define __DICT_H__

#include "ezctypes.h"


void dict_init(dict_t * dict);

void dict_set(dict_t * dict, char * key, obj_t obj);

int dict_index(dict_t * dict, char * key);


#endif