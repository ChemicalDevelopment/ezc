#ifndef __ESTACK_H__
#define __ESTACK_H__

#include "ezctypes.h"


void estack_init(estack_t * stack);

void estack_push(estack_t * stack, obj_t obj);

obj_t estack_pop(estack_t * estack);

obj_t estack_get(estack_t * estack, int i);

#endif