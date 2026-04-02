package edu.mit.csail.sdg.alloy4viz;

import java.util.List;

/**
 * VizTrace encapsulates a trace composed of multiple VizStates (one per time
 * step), and optionally a display name.
 */
public class VizTrace {

    private final String         name;
    private final String         xmlPath;
    private final List<VizState> states;
    private final int            traceLength;
    private final int            loopLength;

    public VizTrace(String name, List<VizState> states, String xmlPath, int traceLength, int loopLength) {
        this.name = name;
        this.states = states;
        this.xmlPath = xmlPath;
        this.traceLength = traceLength;
        this.loopLength = loopLength;
    }

    public String getName() {
        return name;
    }

    public String getXmlPath() {
        return xmlPath;
    }

    public List<VizState> getStates() {
        return states;
    }

    public VizState getState(int idx) {
        return states.get(idx);
    }

    public int length() {
        return states.size();
    }

    public int getTraceLength() {
        return traceLength;
    }

    public int getLoopLength() {
        return loopLength;
    }
}
