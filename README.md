# DataEngine for ComicRack

DataEngine provides a way to move ComicRack's data in and out of other structured formats.

The DataEngine's default configuration can be massively and instantly destructive to your CR database. Take backups.

## de.py main program options
```bash
--config /path/to/crde.cfg
```
optional, path to config file, no config exists by default
```bash
--crdb /path/to/ComicDb.xml
```
optional, path to ComicRack database, defaults to %appdata%/cYo/ComicRack/ComicDb.xml.
```bash
--dry-run, -N
```
optional, flag to disable all actions that actually DO anything. This is supposed to be safe...
```bash
--verbose, -V
```
optional, flag to be more noisy than usual, but less than debug output
```bash
--debugging
```
optional, flag to activate debug mode.

## de.py commands

### export
______
```bash
export /to/path/
```
Export data from crdb to *path*. DE will attempt to create intermediate folders as needed, and will overwrite existing files in the destination if they clash. DE will create a *UUID*.xml for each book in the database. The exported xml files are not the same structure as a ComicInfo.xml file.
```bash
--id id
```
optional, export the *id* specified. multiple values allowed. **If this is omitted, the entire DB will be exported.**

### import
___
```bash
import /from/path/
```
Import data from *path* to crdb. DE does not verify that the data quality is good - only that the structure is valid to ComicRack. That is a very low bar. DE will replace existing records.
```bash
--id id
```
optional, only import specified *id*.
```bash
--safe
```
optional, flag to disable overwriting existing data. Existing UUIDs will be skipped and will generate a warning.

### repack
___
```bash
repack origin destination
```

Crawls *origin* and copies the books to *destination*, converting rars to zips.

```bash
--rar-only, -R
```
Copies only rar files.
```bash
--replace, --forced, -F
```
Enables the repack process to replace existing files. It'll nuke everything under *destination* if you screw up. You've been warned.
## experimental functions
bench
___
```bash
bench
```
Generate some numbers about how fast we can process your database. YMMV. SSDs are heat-sensitive...

crunch
___
```bash
crunch
```
Run the internal test function. You probably don't want to do this.

