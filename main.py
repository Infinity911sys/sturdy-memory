"""
CHAD OS – Phase 2.0 Single-File Build
- Event loop
- Command router
- Simple apps
- Status + log commands
- Continuity history
- No imports, no folders
"""

# =========================
# CONFIG (EMBEDDED)
# =========================

chad_os_config = """
system:
  name: "CHAD-OS"
  phase: "2.0-single-file"
  version: "0.3.0"
  description: "AI-native OS with command router and simple apps."
boot:
  ticks: 20
"""

# =========================
# KERNEL
# =========================

class MessageBus:
    def __init__(self):
        self._queue = []

    def publish(self, message):
        self._queue.append(message)

    def process_pending(self):
        self._queue.clear()


class Scheduler:
    def tick(self):
        pass


class EventLoop:
    def __init__(self):
        self._tick_count = 0

    def tick(self):
        self._tick_count += 1
        return self._tick_count


def bootstrap_system():
    return {
        "message_bus": MessageBus(),
        "scheduler": Scheduler(),
        "event_loop": EventLoop(),
    }


# =========================
# SERVICES
# =========================

class ServiceRegistry:
    def __init__(self):
        self._services = {}

    def register(self, name, service):
        self._services[name] = service

    def get(self, name):
        return self._services.get(name)


class IdentityService:
    def __init__(self):
        self._system_id = "CHAD-OS"

    def get_system_id(self):
        return self._system_id


class MemoryService:
    def __init__(self):
        self._store = {}

    def set(self, key, value):
        self._store[key] = value

    def get(self, key, default=None):
        return self._store.get(key, default)


class ContextEngine:
    def __init__(self, memory_service):
        self._memory = memory_service
        self._context = {}

    def set_context(self, key, value):
        self._context[key] = value

    def snapshot(self):
        return dict(self._context)


class EventService:
    def __init__(self, message_bus):
        self._bus = message_bus

    def emit(self, event_type, payload=None):
        self._bus.publish({"type": event_type, "payload": payload or {}})


class ContinuityService:
    def __init__(self, identity_graph):
        self._graph = identity_graph

    def record_event(self, actor_id, data):
        self._graph.add_event(actor_id, data)


# =========================
# CONTINUITY
# =========================

class IdentityGraph:
    def __init__(self):
        self._events = []

    def add_event(self, actor_id, data):
        self._events.append({"actor": actor_id, "data": data})

    def all_events(self):
        return list(self._events)


class StatePersistence:
    def save(self, state):
        pass

    def load(self):
        return {}


# =========================
# INTELLIGENCE
# =========================

class HeuristicEngine:
    def decide(self, signal):
        cmd = signal.get("command") or ""
        if cmd.startswith("app "):
            return "route_app"
        if cmd in ("status", "log", "help", "exit"):
            return "handle_system_command"
        if cmd.strip():
            return "handle_generic_command"
        return "idle"


class PredictionEngine:
    def predict(self, signal):
        return {"risk": "low"}


class ReasoningCore:
    def __init__(self, heuristic_engine, prediction_engine):
        self._heuristic = heuristic_engine
        self._prediction = prediction_engine

    def process(self, signal):
        return {
            "decision": self._heuristic.decide(signal),
            "prediction": self._prediction.predict(signal),
        }


class AdaptiveHooks:
    def adapt(self, result):
        pass


# =========================
# UI
# =========================

class RenderingEngine:
    def render(self, message):
        print(message)


class InteractionModel:
    def get_input(self):
        try:
            return input("CHAD-OS> ")
        except:
            return None


# =========================
# SYSTEM TOOLS / APPS
# =========================

def system_heartbeat():
    return "Heartbeat OK"


class AppRegistry:
    def __init__(self):
        self._apps = {}

    def register(self, name, func):
        self._apps[name] = func

    def get(self, name):
        return self._apps.get(name)


def app_echo(args, renderer):
    if not args:
        renderer.render("[app:echo] Nothing to echo.")
    else:
        renderer.render("[app:echo] " + " ".join(args))


def app_calc(args, renderer):
    if len(args) != 3:
        renderer.render("[app:calc] Usage: app calc <a> <b>")
        return
    try:
        a = float(args[1])
        b = float(args[2])
        renderer.render(f"[app:calc] {a} + {b} = {a + b}")
    except:
        renderer.render("[app:calc] Invalid numbers.")


def app_note(args, renderer, memory):
    if len(args) < 2:
        renderer.render("[app:note] Usage: app note <text>")
        return
    text = " ".join(args[1:])
    notes = memory.get("notes", [])
    notes.append(text)
    memory.set("notes", notes)
    renderer.render(f"[app:note] Saved note #{len(notes)}")


def app_notes_list(renderer, memory):
    notes = memory.get("notes", [])
    if not notes:
        renderer.render("[app:note] No notes yet.")
        return
    renderer.render("[app:note] Notes:")
    for i, n in enumerate(notes, 1):
        renderer.render(f"  {i}. {n}")


# =========================
# COMMAND ROUTER
# =========================

class CommandRouter:
    def __init__(self, renderer, app_registry, memory, continuity, identity):
        self.renderer = renderer
        self.apps = app_registry
        self.memory = memory
        self.continuity = continuity
        self.identity = identity

    def handle(self, cmd, tick):
        if cmd is None:
            return False

        cmd = cmd.strip()
        if not cmd:
            return False

        if cmd == "help":
            self._help()
        elif cmd == "status":
            self._status(tick)
        elif cmd == "log":
            self._log()
        elif cmd == "notes":
            app_notes_list(self.renderer, self.memory)
        elif cmd == "exit":
            self.renderer.render("Exiting CHAD-OS loop.")
            return True
        elif cmd.startswith("app "):
            self._route_app(cmd)
        else:
            self._generic(cmd)

        self.continuity.record_event(
            actor_id=self.identity.get_system_id(),
            data={"tick": tick, "command": cmd, "type": "command_handled"},
        )
        return False

    def _help(self):
        self.renderer.render("Available commands:")
        self.renderer.render("  help        - show this help")
        self.renderer.render("  status      - show system status")
        self.renderer.render("  log         - show recent continuity events")
        self.renderer.render("  notes       - list saved notes")
        self.renderer.render("  app echo X  - echo text")
        self.renderer.render("  app calc a b- add two numbers")
        self.renderer.render("  app note X  - save a note")
        self.renderer.render("  exit        - exit loop")

    def _status(self, tick):
        self.renderer.render(f"[status] Tick: {tick}")
        self.renderer.render(f"[status] System: {self.identity.get_system_id()}")

    def _log(self):
        self.renderer.render("[log] (Use future expansion to show full history.)")

    def _route_app(self, cmd):
        parts = cmd.split()
        if len(parts) < 2:
            self.renderer.render("[router] Usage: app <name> ...")
            return
        app_name = parts[1]
        args = parts[1:]
        app = self.apps.get(app_name)
        if not app:
            self.renderer.render(f"[router] Unknown app: {app_name}")
            return
        if app_name == "note":
            app(args, self.renderer, self.memory)
        else:
            app(args, self.renderer)

    def _generic(self, cmd):
        self.renderer.render(f"[generic] You said: {cmd}")


# =========================
# MAIN BOOT SEQUENCE
# =========================

def main():
    kernel = bootstrap_system()
    message_bus = kernel["message_bus"]
    scheduler = kernel["scheduler"]
    event_loop = kernel["event_loop"]

    registry = ServiceRegistry()
    identity = IdentityService()
    memory = MemoryService()
    context = ContextEngine(memory)
    events = EventService(message_bus)

    identity_graph = IdentityGraph()
    continuity = ContinuityService(identity_graph)
    persistence = StatePersistence()

    registry.register("identity", identity)
    registry.register("memory", memory)
    registry.register("context", context)
    registry.register("events", events)
    registry.register("continuity", continuity)
    registry.register("persistence", persistence)

    heuristic = HeuristicEngine()
    prediction = PredictionEngine()
    reasoning = ReasoningCore(heuristic, prediction)
    adaptive = AdaptiveHooks()

    renderer = RenderingEngine()
    interaction = InteractionModel()

    apps = AppRegistry()
    apps.register("echo", app_echo)
    apps.register("calc", app_calc)
    apps.register("note", app_note)

    router = CommandRouter(renderer, apps, memory, continuity, identity)

    renderer.render("=== CHAD OS Phase 2.0 Booting ===")
    renderer.render(system_heartbeat())

    max_ticks = 20
    for tick in range(1, max_ticks + 1):
        renderer.render(f"[Tick {tick}]")
        user_cmd = interaction.get_input()

        context.set_context("command", user_cmd)
        context.set_context("tick", tick)
        context.set_context("system_id", identity.get_system_id())

        signal = context.snapshot()
        result = reasoning.process(signal)
        adaptive.adapt(result)

        decision = result["decision"]

        continuity.record_event(
            actor_id=identity.get_system_id(),
            data={"tick": tick, "decision": decision, "command": user_cmd},
        )

        exit_requested = router.handle(user_cmd or "", tick)
        if exit_requested:
            break

        scheduler.tick()
        event_loop.tick()
        message_bus.process_pending()

    renderer.render("=== CHAD OS Phase 2.0 Complete ===")
    renderer.render(f"Continuity events recorded: {len(identity_graph.all_events())}")


if __name__ == "__main__":
    main()
