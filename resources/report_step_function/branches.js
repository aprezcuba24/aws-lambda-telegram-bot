QUERIES = {
  public_actions: 'filter (is_group=1) | stats count(*) as calls',
  private_actions: 'filter (is_group=0) | stats count(*) as calls',
  new_user: 'filter (is_new_user=1) | stats count(*) as calls',
}

module.exports = async () => {
  return Object.entries(QUERIES).map(([code, query]) => ({
    StartAt: code,
    States: {
      [code]: {
        Type: 'Pass',
        Result: { code, query },
        Next: `${code}_calculate`
      },
      [`${code}_calculate`]: {
        Type: 'Task',
        Resource: {
          'Fn::GetAtt': ['calculate_report_data', 'Arn']
        },
        End: true
      }
    }
  }))
}
