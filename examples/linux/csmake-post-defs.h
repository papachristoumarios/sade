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

// Marios 
#define __builtin_bswap32(x) (x)
#define __builtin_bswap64(x) (x)
#define __builtin_bswap16(x) (x)

#define __int128 long
#define __builtin_types_compatible_p(x,y) 1
#define __extension
#define __extension__ 
#define __attribute__(x)
#define __restrict

#define __builtin_object_size(x,y) 1
#define __builtin___memcpy_chk(x,y,z,w) 1
#define __builtin___memmove_chk(x,y,z,w) 1
#define __builtin___memset_chk(x,y,z,w) 1
#define __builtin___mempcpy_chk(x,y,z,w) 1
#define __builtin___strcpy_chk(x,y,z) 1
#define __builtin___strncpy_chk(x,y,z,w) 1
#define __builtin___stpcpy_chk(x,y,z) 1
#define __builtin___strcat_chk(x,y,z) 1
#define __builtin___strncat_chk(x,y,z,w) 1

#define __builtin___sprintf_chk(x,y,z,w,...) 1
#define __builtin___vsprintf_chk(x,y,z,w,r) 1
#define __builtin___snprintf_chk(x,y,z,w) 1
#define __builtin___printf_chk(x,y,...) 1
#define __builtin___vprintf_chk(x,y,z) 1
#define __builtin___fprintf_chk(x,y,z,...) 1
#define __builtin___vsnprintf_chk(x,y,z,w,r) 1
#define __builtin_strchr(x,y) 1
#define __builtin_va_arg_pack() 1
#define __builtin_strlen(x) 1
#define __builtin_strcmp(x,y) 1
#define __builtin_va_arg_pack_len() 1
#define __builtin_va_start(x,y) 1
#define __builtin_unreachable() 1
#define __builtin_mul_overflow(x,y,z) 1
#define __builtin_add_overflow(x,y,z) 1
#define __builtin_choose_expr(a,v,c) 1
#define __builtin_strcspn(x,y) 1
#define __builtin_return_address(x) 1
#define __builtin_memset(x,y,z) 1
#define __COUNTER__ 0

// Marios

#define __builtin_memcmp(x,y,z) 1

#define __volatile__ volatile
#define __alignof__ sizeof

// To make it appear as a read-only identifier */
int main();
/* To avoid unused include file warnings */
static void _cscout_dummy1(void) { _cscout_dummy1(); }
