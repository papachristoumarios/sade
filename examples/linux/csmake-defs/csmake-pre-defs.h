/*
 * (C) Copyright 2001-2003 Diomidis Spinellis.
 *
 * Standard definitions read when starting up
 * Generic gcc version
 *
 * To create this file look at /usr/lib/gcc-lib/ * / * /specs
 * This file should have read-only permissions
 *
 * $Id: defs.h 1.12 2002/12/25 19:35:42 dds Exp $
 */

#define __DATE__  "Jan 01 1970"
#define __TIME__ "12:34:56"
#define __FILE__ "UNKNOWN.c"
#define __func__ "UNKNOWN"
#define __LINE__ 1
#define __PRETTY_FUNCTION__ "UNKNOWN"
#define __func__ "UNKNOWN"

#define __STDC__ 1

#ifdef __cplusplus
#define __EXCEPTIONS
#endif

/* Generic gcc workarounds */
// asm might be not needed
#define asm __asm__
#define typeof __typeof__
#define __attribute(_x) __attribute__(_x)
#define __builtin_next_arg(_x) 0
#define __builtin_stdarg_start
#define __builtin_va_arg(_ap, _type) (*(_type *)(_ap))
#define __builtin_va_end
#define __builtin_va_list void *
#define __builtin_va_copy(_a, _b)
#define __builtin_constant_p(_x) 0
#define __builtin_frame_address(_x) ((void *)0)
#define __builtin_expect(_a, _b) ((_b), (_a))
#define __builtin_offsetof(s, m) (0)
#define __builtin_memcpy(d, s, n) (d)

#define __extension
#define __extension__

/* To make it appear as a read-only identifier */
int main();
/* To avoid unused include file warnings */
static void _cscout_dummy1(void) { _cscout_dummy1(); }

