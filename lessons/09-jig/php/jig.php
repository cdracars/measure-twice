<?php

declare(strict_types=1);

// The entry point: the only code that touches the real terminal. Given.

require __DIR__ . '/cli.php';

$output = run(array_slice($argv, 1));
fwrite(STDOUT, $output->stdout);
fwrite(STDERR, $output->stderr);
exit($output->code);
