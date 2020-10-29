# Activation du mode debug.



Dans le repertoire **/etc/rgm/thruk/**

Ajouter le fichier **log4perl.conf** tel que:

```
################################
## Logging Configuration
#
# see http://search.cpan.org/perldoc?Log%3A%3ALog4perl%3A%3AConfig
# for other configuration options
#
# normal logging, error messages and sent commands
log4perl.logger=ALL, DebugLog

# enable this line to enable debug logging
# start "./script/thruk_server.pl -d" with -d to enable debugging
#log4perl.logger=ALL, ThrukLog, DebugLog, Screen
# you have to uncomment the logger definitions below too

# normal log messages
#log4perl.appender.ThrukLog=Log::Log4perl::Appender::File
#log4perl.appender.ThrukLog.filename=logs/error.log
##log4perl.appender.ThrukLog.mode=append
#log4perl.appender.ThrukLog.Threshold=INFO
#log4perl.appender.ThrukLog.layout=Log::Log4perl::Layout::PatternLayout
#log4perl.appender.ThrukLog.layout.ConversionPattern=[%d][%H][%p] %m{chomp}%n

## debug too
log4perl.appender.DebugLog=Log::Log4perl::Appender::File
log4perl.appender.DebugLog.filename=/srv/rgm/thruk/logs/debug.log
log4perl.appender.DebugLog.mode=append
log4perl.appender.DebugLog.Threshold=DEBUG
log4perl.appender.DebugLog.layout=Log::Log4perl::Layout::PatternLayout
log4perl.appender.DebugLog.layout.ConversionPattern=[%d][%H][%p] %m{chomp}%n

## screen logger
#log4perl.logger                    = DEBUG, Screen
#log4perl.appender.Screen           = Log::Log4perl::Appender::Screen
#log4perl.appender.Screen.stderr    = 1
#log4perl.appender.Screen.Threshold = DEBUG
#log4perl.appender.Screen.layout    = Log::Log4perl::Layout::PatternLayout
#log4perl.appender.Screen.layout.ConversionPattern = [%d][%H][%p] %m{chomp}%n

```



Dans le fichier **/srv/rgm/thruk/script/thruk_fastcgi.pl** il faut ajouter la ligne **$ENV{'THRUK_VERBOSE'} = 4;** tel que:

```
#!/usr/bin/env perl

use lib "/srv/rgm/thruk/lib";
use lib "/srv/rgm/thruk/local-lib/lib/perl5";

use strict;
use warnings;
use lib 'lib';

###################################################
# create connection pool
# has to be done really early to save memory
BEGIN {
    $ENV{'THRUK_SRC'} = 'FastCGI';
                $ENV{'THRUK_VERBOSE'} = 4;
    $ENV{'PLACK_ENV'} = 'deployment' unless $ENV{'PLACK_ENV'};
    use Thruk::Backend::Pool;
    Thruk::Backend::Pool::init_backend_thread_pool();
}

use Plack::Handler::FCGI;
use Thruk;
my $server = Plack::Handler::FCGI->new(
    nproc  => 1,
    detach => 1,
);
$server->run(Thruk->startup);

```



Créer le fichier de debug tel que:

```
touch /srv/rgm/thruk/logs/debug.log
chown apache:apache /srv/rgm/thruk/logs/debug.log
```

