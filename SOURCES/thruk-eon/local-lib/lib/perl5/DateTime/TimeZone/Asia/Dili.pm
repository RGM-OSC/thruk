# This file is auto-generated by the Perl DateTime Suite time zone
# code generator (0.07) This code generator comes with the
# DateTime::TimeZone module distribution in the tools/ directory

#
# Generated from /tmp/8FT049ktOU/asia.  Olson data version 2015d
#
# Do not edit this file directly.
#
package DateTime::TimeZone::Asia::Dili;
$DateTime::TimeZone::Asia::Dili::VERSION = '1.88';
use strict;

use Class::Singleton 1.03;
use DateTime::TimeZone;
use DateTime::TimeZone::OlsonDB;

@DateTime::TimeZone::Asia::Dili::ISA = ( 'Class::Singleton', 'DateTime::TimeZone' );

my $spans =
[
    [
DateTime::TimeZone::NEG_INFINITY, #    utc_start
60305269060, #      utc_end 1911-12-31 15:37:40 (Sun)
DateTime::TimeZone::NEG_INFINITY, #  local_start
60305299200, #    local_end 1912-01-01 00:00:00 (Mon)
30140,
0,
'LMT',
    ],
    [
60305269060, #    utc_start 1911-12-31 15:37:40 (Sun)
61256530800, #      utc_end 1942-02-21 15:00:00 (Sat)
60305297860, #  local_start 1911-12-31 23:37:40 (Sun)
61256559600, #    local_end 1942-02-21 23:00:00 (Sat)
28800,
0,
'TLT',
    ],
    [
61256530800, #    utc_start 1942-02-21 15:00:00 (Sat)
61369628400, #      utc_end 1945-09-22 15:00:00 (Sat)
61256563200, #  local_start 1942-02-22 00:00:00 (Sun)
61369660800, #    local_end 1945-09-23 00:00:00 (Sun)
32400,
0,
'JST',
    ],
    [
61369628400, #    utc_start 1945-09-22 15:00:00 (Sat)
62335580400, #      utc_end 1976-05-02 15:00:00 (Sun)
61369660800, #  local_start 1945-09-23 00:00:00 (Sun)
62335612800, #    local_end 1976-05-03 00:00:00 (Mon)
32400,
0,
'TLT',
    ],
    [
62335580400, #    utc_start 1976-05-02 15:00:00 (Sun)
63104803200, #      utc_end 2000-09-16 16:00:00 (Sat)
62335609200, #  local_start 1976-05-02 23:00:00 (Sun)
63104832000, #    local_end 2000-09-17 00:00:00 (Sun)
28800,
0,
'WITA',
    ],
    [
63104803200, #    utc_start 2000-09-16 16:00:00 (Sat)
DateTime::TimeZone::INFINITY, #      utc_end
63104835600, #  local_start 2000-09-17 01:00:00 (Sun)
DateTime::TimeZone::INFINITY, #    local_end
32400,
0,
'TLT',
    ],
];

sub olson_version {'2015d'}

sub has_dst_changes {0}

sub _max_year {2025}

sub _new_instance {
    return shift->_init( @_, spans => $spans );
}



1;

