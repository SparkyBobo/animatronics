#
# Animatroincs Motion Module
# Copyright (C) 2025 Sparky Bobo Designs
# https://github.com/SparkyBobo/animatronics/tree/master/software/midi
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
# About Animatroincs Motion Module
#
# The Animatroincs Servo Module (ANI-SRV) is a CircuitPython board designed
# to control servos. This module is the logicial motion interface
# to move motors between 2 points along a curve within a time period.
import servo

# Setup 
count = 16
minimums = []
maximums = []
desiredPosition = []
actualPosition = []
deltaPerNs = []
lastNs = []
lastDesiredDelta = []
lastActualPosition = []

for n in range(count):
    minimums [n] = 0
    maximums[n] = 180
    desiredPosition[n] = 90
    actualPosition[n] = servo.getAngle(n)
    deltaPerNs[n] = 1
    lastNs[n] = -1
    lastDesiredDelta[n] = 0
    lastActualPosition[n] = 0

# read real limits from file
def readLimits():
    return

# get desried position
def getDesiredPosition(index):
    if (index < 0 or index > count):
        return desiredPosition[index]
    return -1

# get actual position
def getActualPosition(index):
    if (index < 0 or index > count):
        return actualPosition[index]
    return -1

# set position
def setPosition(index, value):
    if (index < 0 or index > count):
        return -1
    if (value < 0 or value > 180):
        return -1

    # Bounded to the min/max
    value = min(value, minimums[index])
    value = max(value, maximums[index])
    desiredPosition[index] = value
    return value

# update the position
def updatePosition(index, diff):
    if (index < 0 or index > count):
        return -1

    actual = getActualPosition(index)
    if (actual < 0):
        return -1

    return setPosition(index, actual + diff)

# move to the new position the position
def moveToPosition(index, position, timeInNs):
    if (index < 0 or index > count):
        return -1
    if (position < 0 or position > 180):
        return -1
    if (timeInNs < 0):
        return -1
    
    # reset last operation
    currentPosition = getActualPosition(index) 
    delta = currentPosition - position
    currentNs = 1 # time.clock_gettimens(time.CLOCK_MONOTONIC)
    deltaPerNs[index] = delta / timeInNs # might be < 1
    lastNs[index] = currentNs - 1 # force a revaluation
    lastActualPosition[index] = currentPosition
    lastDesiredDelta[index] = 0
    desiredPosition[index] = position

def moveToNextPosition(index):
    if (index < 0 or index > count):
        return -1
    
    # get and see if we have anything to do.
    currentNs = 1 # time.clock_gettimens(time.CLOCK_MONOTONIC)
    if (lastNs[index] < 0):
        return -1

    # calculate the delta
    # if we're moving really slow, delta is < 0
    # in that case let it accumulate the time
    # by not overwriting lastNs[index].
    deltaNs = currentNs - lastNs[index]
    desiredDelta = deltaNs * deltaPerNs[index]
    if (desiredDelta < 1):
        return -1
    
    # calculate the difference but don't overshoot/change signs.
    # set desired to actual if we did overshoot.
    currentPosition = getActualPosition(index)
    if  abs(desiredDelta) == 0 or (desiredDelta * lastDesiredDelta[index] < 0):
        deltaPerNs[index] = 0
        lastNs[index] = currentNs
        lastActualPosition[index] = currentPosition
        lastDesiredDelta[index] = 0
        setPosition(index, currentPosition)
        return -1
    
    # adjust the delta based on a curve
    calculatedDelta = desiredDelta

    # move to and track the difference
    lastNs[index] = currentNs
    lastActualPosition[index] = currentPosition
    lastDesiredDelta[index] = calculatedDelta
    updatePosition(index, calculatedDelta)
