<?php

Sugarcrm\Sugarcrm\Console\CommandRegistry\CommandRegistry::getInstance()
    ->addCommand(new Sugarcrm\Sugarcrm\custom\Console\Command\PruneDatabase());
