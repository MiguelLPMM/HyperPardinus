package kodkod.instance;

import java.util.List;

/**
 * Thread-local stash for extra TemporalInstances produced by the hyper-solver.
 * Lives in kodkod.instance so both the native solver and the application
 * layer can reach it with no new dependencies.
 */
public final class HyperTraceStash {
    private HyperTraceStash() {}

    public static final ThreadLocal<List<TemporalInstance>> extraTraces = new ThreadLocal<>();
}