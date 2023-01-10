<?php
namespace Sugarcrm\Sugarcrm\custom\Console\Command;

use DBManagerFactory;
use SugarConfig;
use Sugarcrm\Sugarcrm\Dbal\Connection;
use Symfony\Component\Console\Command\Command;
use Sugarcrm\Sugarcrm\Console\CommandRegistry\Mode\InstanceModeInterface;
use Symfony\Component\Console\Output\OutputInterface;
use Symfony\Component\Console\Input\InputInterface;

class PruneDatabase extends Command implements InstanceModeInterface
{
    protected $preservedTables = array('acl_actions', 'acl_fields',
                    'acl_roles',
                    'acl_roles_actions',
                    'acl_role_sets',
                    'acl_role_sets_acl_roles',
                    'acl_roles_users',
                    'config',
                    'currencies',
                    'custom_fields',
                    'eapm',
                    'expressions',
                    'fields_meta_data',
                    'relationships',
                    'roles',
                    'roles_modules',
                    'roles_users',
                    'team_memberships',
                    'team_notices',
                    'team_sets',
                    'team_sets_modules',
                    'team_sets_teams',
                    'teams',
                    'upgrade_history',
                    'user_preferences',
                    'users');

    protected function configure()
    {
        $this->setName('ps:prunedb')
            ->setDescription('Pune the Sugar database')
            ->setHelp('This command accepts no paramters')
        ;
    }

    protected function execute(InputInterface $input, OutputInterface $output)
    {
        $output->writeln("Pruning database...");
        if ($this->pruneDatabase()){
            $output->writeln("...finished successfully.");
        } else {
            $output->writeln("...failed!");
        }
        return 1;
    }

    private function pruneDatabase() {
        $pruneBatchSize = SugarConfig::getInstance()->get('prune_job_batch_size', 500);
        $db = DBManagerFactory::getInstance();
        $tables = $db->getTablesArray();
        $conn = DBManagerFactory::getInstance()->getConnection();

        if(!empty($tables)) {
            foreach ($tables as $table) {
                if (in_array($table, $this->preservedTables)) {
                    continue;
                }
                if (in_array($table . '_cstm', $tables)) {
                    $custom_columns = $db->get_columns($table.'_cstm');
                    if (!empty($custom_columns['id_c'])) {
                        while (true) {
                            $ids = $conn->createQueryBuilder()
                                ->select('id')
                                ->from($table)
                                ->setMaxResults($pruneBatchSize)
                                ->execute()
                                ->fetchFirstColumn();
                            if (!is_countable($ids) || count($ids) === 0) {
                                break;
                            }
                            if (!$conn->isAutoCommit()) {
                                $conn->beginTransaction();
                            }
                            $conn->executeUpdate(
                                'DELETE FROM ' . $table . '_cstm WHERE id_c IN (?)',
                                [$ids],
                                [Connection::PARAM_STR_ARRAY]
                            );
                            $conn->executeUpdate(
                                'DELETE FROM ' . $table . ' WHERE id IN (?)',
                                [$ids],
                                [Connection::PARAM_STR_ARRAY]
                            );
                            if (!$conn->isAutoCommit()) {
                                $conn->commit();
                            }
                        }
                        $db->optimizeTable($table . '_cstm');
                    }
                } else {
                    $db->query('DELETE FROM ' . $table);
                    $db->commit();
                }
                $db->optimizeTable($table);
            } // foreach() tables

            return true;
        }
        return false;
    }
}

