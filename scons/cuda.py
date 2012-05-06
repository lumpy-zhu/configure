
"""SCons.Tool.cuda

CUDA Tool for SCons

"""

# Copyright (C) 2011 lumpy.zhu@gmail.com
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

import os
import cc

CUDASuffixes = ['.cu', '.CU']

def generate(env):


    import SCons.Tool
    import SCons.Tool.cc
    static_obj, shared_obj = SCons.Tool.createObjBuilders(env)

    NVCCAction  = SCons.Action.Action("$NVCCCOM",       "$NVCCCOMSTR")
    ShNVCCAction= SCons.Action.Action("$ShNVCCCOM",     "$ShNVCCCOMSTR")

    for suffix in CUDASuffixes:
        static_obj.add_action(suffix, NVCCAction)
        shared_obj.add_action(suffix, ShNVCCAction)
        static_obj.add_emitter(suffix, SCons.Defaults.StaticObjectEmitter)
        shared_obj.add_emitter(suffix, SCons.Defaults.SharedObjectEmitter)
    SCons.Tool.cc.add_common_cc_variables(env)


    env['NVCC']       = 'nvcc'    
    env['LINK']       = 'nvcc'    
    env['SHCCFLAGS']  = SCons.Util.CLVar('$CCFLAGS -fPIC')

    env['NVCCCOM']     = '$NVCC -o $TARGET -c $CCFLAGS $NVCCFLAGS $_CCCOMCOM $SOURCES'
    env['SHNVCCCOM']   = '$NVCC -o $TARGET -c $SHCCFLAGS $CCFLAGS $NVCCFLAGS $_CCCOMCOM $SOURCES'

    env['ENV']['PATH'] = os.environ['PATH']

def exists(env):
    return env.Detect('nvcc')

