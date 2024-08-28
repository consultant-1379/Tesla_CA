package com.ericsson.PMMB;

import com.ericsson.PMIM.JythonObjectFactory;

public class PMMB {

    public static CLI getInstance() {
        final JythonObjectFactory factory = new JythonObjectFactory(CLI.class, "CLI", "PMMB_CLI");
        return (CLI) factory.createObject();
    }

    public static void main(final String[] args) {
        final CLI cli = getInstance();
        cli.run_command_prompt(args);
    }
}
