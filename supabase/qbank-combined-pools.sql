-- Question pools can be combined: 'incorrect+flagged', 'incorrect+unused', etc. Single pools work as before.
CREATE OR REPLACE FUNCTION public.qb_create_block(p_count integer, p_mode text, p_timed boolean, p_subjects text[] DEFAULT NULL::text[], p_pool text DEFAULT 'unused'::text)
 RETURNS uuid LANGUAGE plpgsql SECURITY DEFINER SET search_path TO 'public'
AS $function$
declare
  uid uuid := public.qb_require();
  ids text[];
  bid uuid;
  parts text[] := string_to_array(coalesce(p_pool, 'unused'), '+');
begin
  if p_count not in (10, 20, 30, 40, 50) then raise exception 'bad_count'; end if;
  if p_mode not in ('learning', 'exam') then raise exception 'bad_mode'; end if;
  if cardinality(parts) = 0 or not (parts <@ array['unused', 'incorrect', 'flagged', 'all']) then raise exception 'bad_pool'; end if;
  if p_subjects is not null and cardinality(p_subjects) = 0 then p_subjects := null; end if;

  select array_agg(id) into ids from (
    select q.id
    from public.qb_questions q
    left join public.qb_status s on s.question_id = q.id and s.user_id = uid
    where q.active
      and (p_subjects is null or q.subject = any(p_subjects))
      and ('all' = any(parts)
           or ('unused' = any(parts) and s.question_id is null)
           or ('incorrect' = any(parts) and s.last_correct = false)
           or ('flagged' = any(parts) and coalesce((select r.flagged from public.qb_responses r
                                               where r.user_id = uid and r.question_id = q.id
                                               order by r.updated_at desc limit 1), false)))
    order by random()
    limit p_count) pick;

  if ids is null then raise exception 'no_questions'; end if;

  insert into public.qb_blocks (user_id, mode, timed, time_limit_sec, question_ids, subjects, pool)
  values (uid, p_mode, coalesce(p_timed, false),
          case when p_timed then cardinality(ids) * 90 end, ids, p_subjects, p_pool)
  returning id into bid;

  -- flags carry over: a question flagged the last time it was seen starts flagged here too
  insert into public.qb_responses (block_id, user_id, question_id, idx, flagged)
  select bid, uid, t.qid, t.ord - 1, true
  from unnest(ids) with ordinality as t(qid, ord)
  where coalesce((select r.flagged from public.qb_responses r
                  where r.user_id = uid and r.question_id = t.qid and r.block_id <> bid
                  order by r.updated_at desc limit 1), false);
  return bid;
end;
$function$;
select 'pools ready' as status;
