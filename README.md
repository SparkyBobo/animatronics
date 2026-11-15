# Animacy

**A platform for building animatronic performers and bringing them to life.**

Animacy is an evolving framework for creating, controlling, and coordinating animatronic characters. It grew out of DaBones, an animatronic band built to perform music, and the engineering challenges of making multiple characters move, play, and perform together.

What began as software written to bring a particular group of characters to life has grown into a reusable platform: a foundation for building performers, describing their behavior, coordinating their actions, and producing synchronized shows.

The project has two closely connected identities:

- **DaBones** is the original animatronic band and creative performance project.
- **Animacy** is the reusable software framework and supporting platform developed through that work.

DaBones is the reason Animacy exists. Animacy is intended to make it possible to build more than DaBones.

## DaBones: The Original Project

DaBones is an animatronic band created to perform music with animated characters. The project combines mechanical construction, electronics, embedded software, audio playback, lighting, and show control.

The goal is more than making figures move. The characters should appear to perform: singing, playing instruments, moving in time with music, and expressing personality through coordinated motion.

Building DaBones brings together several disciplines:

- Character design and mechanical construction
- Motors, actuators, and motion control
- Embedded electronics and firmware
- Musical performance data and MIDI
- Audio playback and synchronization
- Stage lighting and effects
- Show coordination and control

The original project provided the real-world requirements that shaped the framework. Each new capability was motivated by something the performers needed to do.

DaBones remains the creative project and the proving ground for Animacy.

## Animacy: The Framework

Animacy is a reusable software platform for controlling animatronic performers.

It provides a common approach to translating performance input into character behavior and ultimately into commands for physical hardware.

Rather than implementing every character as a collection of one-off scripts, Animacy aims to provide shared concepts and infrastructure. Characters can have different mechanical arrangements and capabilities while participating in a common performance system.

The framework is designed for CircuitPython and resource-constrained embedded hardware. Memory consumption, allocation overhead, predictable execution, and clear separation of responsibilities are important engineering considerations.

### Design Goals

- **Reusable character control** — share common control and behavior patterns across different performers.
- **Performance-driven behavior** — translate music and other performance input into meaningful character actions.
- **Synchronized performance** — coordinate multiple characters and their actions against a common timeline.
- **Hardware abstraction** — separate character behavior and performance logic from the details of individual hardware devices.
- **Extensible architecture** — add performers, behaviors, drivers, and capabilities without redesigning the entire system.
- **Embedded practicality** — work within the memory and execution constraints of microcontroller-based hardware.
- **Testability** — make behavior and hardware interactions understandable and testable outside the physical performance environment.

### Architectural Approach

Animacy separates the intent of a performance from its physical execution.

At a high level, the system transforms performance input into domain-level messages, dispatches those messages to the appropriate behavior, plans the resulting actions, evaluates them, and sends commands through hardware drivers.

The architecture includes several distinct responsibilities:

- **Performance messages** describe events occurring during a performance.
- **Behavior dispatching** determines how performers respond to those events.
- **Planning** translates behavior into planned actions.
- **Evaluation** determines the commands required to carry out those actions.
- **Driver dispatching** sends commands to the appropriate hardware.

This separation keeps musical and character behavior from becoming tightly coupled to individual motors, controllers, or other devices.

It also provides a foundation for desktop simulations and other tools that can observe driver output, inspect values, and understand how constraints affect behavior without requiring the actual hardware.

The architecture continues to evolve as real performance requirements expose new needs.

## Performance Capabilities

Animacy is being developed to support a coordinated show environment, not simply isolated character motion.

The broader performance system includes several related capabilities.

### Character Motion and Expression

Characters need to move in ways that support their personality and role in the performance.

This includes mechanisms such as head movement, mouth movement, and other character-specific actions. Different characters may have different hardware and capabilities while sharing common software concepts.

### Musical Performance and MIDI

MIDI provides a useful way to describe musical events and synchronize character actions with music.

Animacy translates incoming performance information into domain-level events that can be interpreted by character behavior. This keeps the musical input format separate from the character's implementation.

### Audio Playback

Audio is part of the performance itself. Playback needs to be coordinated with the characters and the show timeline.

The larger system is intended to support audio playback control as a first-class part of a performance.

### Lighting and Effects

Lighting and other stage effects contribute to the overall show. They need to be coordinated with the musical and character performance rather than treated as unrelated equipment.

### Multiple Performers

A central goal is to coordinate several animatronic characters as one ensemble.

The system needs shared timing and a common way to describe and distribute performance events, while allowing each character to interpret those events according to its own capabilities.

## Hardware and Software

Animacy is built around CircuitPython-capable embedded hardware, with the Raspberry Pi Pico and RP2040 family playing an important role.

The project also includes supporting hardware and software for:

- Character-specific controllers and electronics
- MIDI input and performance messaging
- DMX lighting control
- Audio playback
- Show-file preparation and transfer
- Desktop-side development, testing, and simulation

Not every part of the larger show system belongs inside the framework itself. Animacy provides the common software foundation, while supporting devices and tools provide specialized capabilities.

## Development Philosophy

Animacy is being developed through the practical demands of building and operating real performers.

The framework should be reusable, but it should not become an abstraction exercise detached from the physical system it serves.

Engineering decisions are informed by several principles:

- Prefer shared concepts over duplicated character-specific implementations.
- Keep responsibilities separate and interfaces understandable.
- Design for the actual constraints of embedded hardware.
- Make behavior observable and testable.
- Preserve flexibility as the creative requirements evolve.
- Build capabilities that make the performers and the show better.

The project is both a software platform and an ongoing engineering effort. Its architecture and capabilities will continue to develop as new performance ideas and hardware requirements emerge.

## Project Status and Direction

Animacy has already supported the development and operation of the DaBones Halloween show.

The Halloween 2026 performance represents an important milestone: the platform moved beyond experimentation and was used in a real coordinated performance.

The next stage is to strengthen the foundation, improve the existing capabilities, and expand the system toward a more ambitious show.

The longer-term vision is a flexible platform capable of supporting increasingly expressive characters, more sophisticated performance behavior, and a richer synchronized show environment.

This is an evolving platform rather than a fixed product with a predetermined final feature set.

## Repository

This repository contains the Animacy framework and its supporting software.

The repository's development history reflects the evolution from the original DaBones-specific implementation toward a reusable platform.

For implementation details, current work, investigations, and planned improvements, see the source code, documentation, and GitHub Issues.

## Names and History

- **DaBones** is the name of the original animatronic band and creative project.
- **Animacy** is the name of the framework that grew out of building DaBones.
- The earlier software project and package name was `dabones`; it was renamed to `animacy` as the framework became more general.

DaBones remains DaBones. Animacy is the platform that helps bring it to life.
