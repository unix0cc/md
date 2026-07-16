# ========== Copyright Header Begin ==========================================
# 
# OpenSPARC T1 Processor File: Makefile
# Copyright (c) 2006 Sun Microsystems, Inc.  All Rights Reserved.
# DO NOT ALTER OR REMOVE COPYRIGHT NOTICES.
# 
# The above named program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public
# License version 2 as published by the Free Software Foundation.
# 
# The above named program is distributed in the hope that it will be 
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public
# License along with this work; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA.
# 
# ========== Copyright Header End ============================================
#
# Copyright 2005 Sun Microsystems, Inc.  All rights reserved.
# Use is subject to license terms.
#
# ident	"@(#)Makefile	1.13	06/06/12 SMI"
#

TOP=..
include $(TOP)/Makefile.master

CONFIGS = 1up 1g32p 1g2p
DBIN_CFGS = $(CONFIGS:%=%-md.bin)
DTXT_CFGS = $(CONFIGS:%=%-md.txt)
HBIN_CFGS = $(CONFIGS:%=%-hv.bin)
HTXT_CFGS = $(CONFIGS:%=%-hv.txt)

all :: $(DBIN_CFGS) $(DTXT_CFGS) $(HBIN_CFGS) $(HTXT_CFGS)

%-md.pp: %.pdesc
	$(CPP) $< $@

%-hv.pp: %.hdesc
	$(CPP) $< $@

%-md.bin: %-md.pp
	$(MDGEN) --binary $(VERBOSE) --outfile $@ $<

%-md.txt: %-md.pp
	$(MDGEN) --text --outfile $@ $<

%-hv.bin: %-hv.pp
	$(MDGEN) --binary $(VERBOSE) --outfile $@ $<

%-hv.txt: %-hv.pp
	$(MDGEN) --text --outfile $@ $<

clean ::
	$(RM) *.pp $(HTXT_CFGS) $(DTXT_CFGS)

clobber ::
	$(RM) $(HBIN_CFGS) $(DBIN_CFGS)

.KEEP_STATE:
